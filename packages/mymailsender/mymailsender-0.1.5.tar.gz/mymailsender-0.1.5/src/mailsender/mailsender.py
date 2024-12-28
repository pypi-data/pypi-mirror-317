# my_mail_sender.py

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
import os
import inspect
import yaml


class MyMailSender:
    def __init__(
        self,
        smtp_server: Optional[str] = None,
        port: Optional[int] = None,
        use_tls: Optional[bool] = None,
        use_ssl: Optional[bool] = None,
        use_auth: Optional[bool] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        config_filename: str = 'mailsender.yaml'
    ):
        """
        Wrapper for sending emails with Python's smtplib and email modules.

        Hvis argumentene ikke er gitt, forsøker den å laste konfigurasjonen fra en YAML-fil
        i samme mappe som skriptet som importerer denne modulen.

        :param smtp_server: SMTP-server, f.eks. "localhost" eller "smtp.mailslurp.com"
        :param port: SMTP-port, f.eks. 25, 587, 465, ...
        :param use_tls: Sett til True hvis du vil kjøre STARTTLS
        :param use_ssl: Sett til True hvis du vil kjøre SSL (SMTPS)
        :param use_auth: Sett til True hvis serveren krever innlogging
        :param username: SMTP-brukernavn (valgfri)
        :param password: SMTP-passord (valgfri)
        :param config_filename: Navnet på konfigurasjonsfilen
        """
        # Last konfigurasjonen fra fil hvis noen argumenter mangler
        config = {}
        if any(arg is None for arg in [smtp_server, port, use_tls, use_ssl, use_auth, username, password]):
            config = self._load_config(config_filename)
        
        # Sett attributter, prioriter argumenter over konfigurasjonsfil
        self.smtp_server = smtp_server or config.get('smtp_server')
        self.port = port or config.get('port')
        self.use_tls = use_tls if use_tls is not None else config.get('use_tls', False)
        self.use_ssl = use_ssl if use_ssl is not None else config.get('use_ssl', False)
        self.use_auth = use_auth if use_auth is not None else config.get('use_auth', False)
        self.username = username or config.get('username')
        self.password = password or config.get('password')

        # Sjekk at nødvendige konfigurasjonsverdier er tilstede
        missing = []
        if not self.smtp_server:
            missing.append('smtp_server')
        if not self.port:
            missing.append('port')
        if self.use_auth and (not self.username or not self.password):
            if not self.username:
                missing.append('username')
            if not self.password:
                missing.append('password')
        if missing:
            raise ValueError(f"Mangler konfigurasjonsverdier: {', '.join(missing)}")

    def _load_config(self, filename: str, config_path: Optional[str] = None) -> dict:
        """
        Laster konfigurasjonen fra en YAML-fil i mappen til skriptet som importerer denne modulen.

        :param filename: Navnet på konfigurasjonsfilen
        :return: Konfigurasjonen som en ordbok
        """
        if config_path:
            config_file = config_path
        else:
            config_file = os.path.join(os.getcwd(), filename)

        print('loading config, config path is:', config_file)

        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                try:
                    config = yaml.safe_load(f)
                    if config is None:
                        config = {}
                    return config
                except yaml.YAMLError as e:
                    raise ValueError(f"Feil ved lasting av konfigurasjonsfil: {e}")
        else:
            return {}

    def send_mail(
        self,
        sender_email: str,
        recipient_emails: List[str],
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None
    ) -> None:
        """
        Sender en e-post med valgfrie vedlegg og HTML-innhold.

        :param sender_email: Avsenderens e-postadresse
        :param recipient_emails: Liste over hovedmottakere
        :param subject: Emnet for e-posten
        :param body_text: Ren-tekst-innhold
        :param body_html: (valgfritt) HTML-innhold
        :param attachments: (valgfritt) Liste over filstier for vedlegg
        :param cc_emails: (valgfritt) Liste over CC-mottakere
        :param bcc_emails: (valgfritt) Liste over BCC-mottakere
        """

        # Opprett MIME-melding
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipient_emails)
        msg["Subject"] = subject

        if cc_emails:
            msg["Cc"] = ", ".join(cc_emails)
        # BCC settes ikke i meldingshodet

        # Legg til ren tekst
        msg.attach(MIMEText(body_text, "plain"))

        # Legg til HTML, hvis gitt
        if body_html:
            msg.attach(MIMEText(body_html, "html"))

        # Legg til vedlegg, hvis gitt
        if attachments:
            for file_path in attachments:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"Vedleggfil ikke funnet: {file_path}")
                with open(file_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = os.path.basename(file_path)  # Filnavnet uten path
                part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
                msg.attach(part)

        # Samle opp alle mottakere
        all_recipients = recipient_emails[:]
        if cc_emails:
            all_recipients.extend(cc_emails)
        if bcc_emails:
            all_recipients.extend(bcc_emails)

        # Koble til SMTP-server med rett protokoll
        if self.use_ssl:
            # SMTPS - ofte port 465
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                self._authenticate(server)
                server.sendmail(sender_email, all_recipients, msg.as_string())
        else:
            # Ren SMTP - ofte port 25 eller 587
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.ehlo_or_helo_if_needed()

                # StartTLS hvis valgt
                if self.use_tls:
                    server.starttls()
                    server.ehlo_or_helo_if_needed()

                # Logg inn hvis valgt
                self._authenticate(server)

                # Send e-posten
                server.sendmail(sender_email, all_recipients, msg.as_string())

        print(f"E-posten er sendt til {all_recipients} med emnet '{subject}'")

    def _authenticate(self, server: smtplib.SMTP) -> None:
        """
        Hjelpefunksjon for å logge inn hvis vi har use_auth=True.
        """
        if self.use_auth and self.username and self.password:
            server.login(self.username, self.password)
