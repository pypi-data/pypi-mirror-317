from pydantic import BaseModel, Field


class LabelMeShape(BaseModel):
    label: str
    points: list[list[float]] = [Field(..., min_items=2, max_items=2)]
    shape_type: str


class LabelMe(BaseModel):
    shapes: list[LabelMeShape]
    image_height: int
    image_width: int


class OutputPaths(BaseModel):
    dataset_path: str
    images_path: str
    images_train_path: str
    images_val_path: str
    images_test_path: str
    labels_path: str
    labels_train_path: str
    labels_val_path: str
    labels_test_path: str


class SplitedDataset(BaseModel):
    test: list[str]
    train: list[str]


class FileNameAndExtension(BaseModel):
    file_name: str
    extension: str


class Polygon(BaseModel):
    points: list[float]
    label_index: int
    label_name: str

    def get_representation(self):
        return f"{self.label_index} {' '.join(map(str, self.points))}"


class ShapeProcessed(BaseModel):
    path: str
    file_name: str
    polygons: list[Polygon]


class ShapesProcessed(BaseModel):
    shapes: list[ShapeProcessed] = []


class YoloYML(BaseModel):
    train: str
    val: str
    test: str
    nc: int
    names: list[str]
