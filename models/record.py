from pydantic import BaseModel


class Record(BaseModel):
    id: int
    img_id: str
    description: str
    img_url: str
    doc_url: str

async def render_record_model(base_record_data: tuple) -> Record:
    return Record(
        id=base_record_data[0],
        img_id=base_record_data[1],
        description=f"{base_record_data[2][:1000]}...",
        img_url=f"https://raw.githubusercontent.com/EvgeniBondarev/LabsData/main/imgs/img_{str(base_record_data[1])[:4]}/{base_record_data[1]}.jpg",
        doc_url=f"https://raw.githubusercontent.com/EvgeniBondarev/LabsData/main/documents/doc_{str(base_record_data[1])[:4]}/{base_record_data[1]}.pdf",
    )
