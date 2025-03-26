from fastapi import FastAPI, BackgroundTasks
from mailer import send_mail
from config import MailBody

app = FastAPI()




@app.get("/")
def index():
    return {"success" : "Fast Api is worked successful"}



@app.post("/send-email")
async def schedule_mail(req: MailBody, tasks: BackgroundTasks):
    data = req.dict()
    tasks.add_task(send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}