from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

ids: list[dict] = json.load(open("data.json"))


@app.get("/", include_in_schema=False)
@app.get("/ids", include_in_schema=False)
def root(request: Request):
    template = templates.get_template("home.html")
    print("TEMPLATE:", template)
    return templates.TemplateResponse(request, "home.html", {"ids": ids, "name": "home"})


@app.get("/api/id")
def get_ids():
    return ids

@app.get("/api/id/{id}")
def get_id(id: int):
    return ids[id]

@app.get("/admin", include_in_schema=False)
def admin_panel(request: Request):
    ids = json.load(open("data.json")) 
    return templates.TemplateResponse(request, "admin.html", {"ids": ids, "name": "admin"})

@app.post("/submit")
async def add_id(username: str = Form(...)):   
    new_id = {
        "id": len(ids),
        "name": username
    }
    ids.append(new_id)
    with open("data.json", "w") as f:
        json.dump(ids, f, indent=4)
    return {"message": "ID added successfully", "id": new_id}

@app.post("/remove")
async def remove_id(remove_id: int = Form(...)):
    ids = json.load(open("data.json"))
    if 0 <= remove_id < len(ids):
        removed_id = ids.pop(remove_id)
        with open("data.json", "w") as f:
            json.dump(ids, f, indent=4)
        return {"message": "ID removed successfully", "id": removed_id}
    else:
        return {"error": "Invalid ID"}