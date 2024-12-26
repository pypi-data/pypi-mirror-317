from fastapi import APIRouter, HTTPException, Body, Path
from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId
from utils.db import mongo_database

template_router = t = APIRouter()

# MongoDB Setup
template_collection = mongo_database["templates"]
variable_collection = mongo_database["variables"]

# Helper function to convert MongoDB ObjectId to string
def to_dict(document):
    """Convert MongoDB document to a dictionary with stringified `_id`."""
    document["_id"] = str(document["_id"])
    return document

# Pydantic Models
class Template(BaseModel):
    id: str = Field(None, alias="_id")  # Use alias to map `_id` field from MongoDB
    name: str = Field(..., title="Template Name", max_length=100)
    subject: str = Field(..., title="Template Subject", max_length=200)
    content: str = Field(..., title="Template Content")

    class Config:
        # allow_population_by_field_name = True  # Allow `_id` to be included in the output as `_id`
        populate_by_name = True  


class TemplateUpdate(BaseModel):
    name: str | None = Field(None, title="Template Name", max_length=100)
    subject: str | None = Field(None, title="Template Subject", max_length=200)
    content: str | None = Field(None, title="Template Content")

class Variable(BaseModel):
    _id: str
    name: str = Field(..., title="Variable Name", max_length=100)

@t.get("/variables", response_model=List[Variable], summary="Fetch all predefined variables")
async def get_variables():
    variables = list(variable_collection.find())
    return [to_dict(variable) for variable in variables]

@t.post("/variables/", response_model=Variable, summary="Create a new predefined variable")
async def create_variable(variable: Variable):
    variable_dict = variable.dict()
    result = variable_collection.insert_one(variable_dict)
    if result.inserted_id:
        return to_dict({**variable_dict, "_id": result.inserted_id})
    raise HTTPException(status_code=500, detail="Failed to create variable")

# Routes
@t.get("/", response_model=List[Template], summary="Fetch all templates")
async def get_templates():
    templates = list(template_collection.find())
    # Convert ObjectId to string for JSON serialization
    for template in templates:
        if "_id" in template:
            template["_id"] = str(template["_id"])
    return templates


@t.get("/{id}", response_model=Template, summary="Fetch a template by ID")
async def get_template_by_id(
    id: str = Path(..., title="Template ID", description="ID of the template to fetch")
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    template = template_collection.find_one({"_id": ObjectId(id)})
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return to_dict(template)

@t.post("/", response_model=Template, summary="Create a new template")
async def create_template(template: Template):
    template_dict = template.dict(exclude={"_id"})  # Exclude _id on create
    result = template_collection.insert_one(template_dict)
    if result.inserted_id:
        return to_dict({**template_dict, "_id": result.inserted_id})
    raise HTTPException(status_code=500, detail="Failed to create template")

@t.put("/{id}", response_model=Template, summary="Edit an existing template")
async def edit_template(
    id: str = Path(..., title="Template ID", description="ID of the template to edit"),
    update_data: TemplateUpdate = Body(...)
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    update_data_dict = {k: v for k, v in update_data.dict().items() if v is not None}
    if not update_data_dict:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    result = template_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data_dict},
        return_document=True
    )
    if result:
        return to_dict(result)
    raise HTTPException(status_code=404, detail="Template not found")

@t.delete("/{id}", summary="Delete a template")
async def delete_template(
    id: str = Path(..., title="Template ID", description="ID of the template to delete")
):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid template ID")
    result = template_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return {"message": "Template deleted successfully"}
    raise HTTPException(status_code=404, detail="Template not found")

