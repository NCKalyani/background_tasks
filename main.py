from fastapi import BackgroundTasks, FastAPI
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler

app = FastAPI()
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string='InstrumentationKey=8e38391f-f2ab-420e-b6d3-55b54ce06dbb'))
logger.setLevel(10)


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        log_data = {
            "custom_dimensions":
                {
                    "text_msg": message,
                    "email": email,
                    "content": content
                }
        }

        email_file.write(content)
        logger.warning('Text Processed Successfully', extra=log_data)


@app.post("/send_notification/{email}")
def send_notification(email: str, background_tasks: BackgroundTasks):
    logger.warning(f"request received for email: {email}")
    background_tasks.add_task(write_notification, email, message="some notification")
    logger.warning(f"request processed for email: {email}")
    return {"message": "Notification sent in the background"}
