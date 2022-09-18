import xml.dom.minidom
import xml.etree.ElementTree as ET
from glob import glob
from os.path import abspath, splitext
from unittest import result
from xml.etree.ElementTree import Comment, Element, SubElement, tostring

import cv2


def create_file_annotation(
    folder: str, file_name: str, path: str, size: tuple, objects: list
):
    root = ET.Element("annotation")
    root.set("verified", "yes")

    ET.SubElement(root, "folder").text = folder
    ET.SubElement(root, "file_name").text = file_name
    ET.SubElement(root, "path").text = path
    source = ET.SubElement(root, "source")
    database = ET.SubElement(source, "database")
    database.text = "Unknown"

    xml_size = ET.SubElement(root, "size")
    height = ET.SubElement(xml_size, "height")
    height.text = str(size[0])
    width = ET.SubElement(xml_size, "width")
    width.text = str(size[1])
    depth = ET.SubElement(xml_size, "depth")
    depth.text = str(size[2])

    ET.SubElement(root, "segmented").text = "0"

    for object in objects:
        xml_object = ET.SubElement(root, "object")

        ET.SubElement(xml_object, "name").text = object["name"]
        ET.SubElement(xml_object, "pose").text = object["pose"]
        ET.SubElement(xml_object, "truncate").text = object["truncate"]
        ET.SubElement(xml_object, "difficult").text = object["difficult"]

        bndbox = ET.SubElement(xml_object, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(object["xmin"])
        ET.SubElement(bndbox, "ymin").text = str(object["ymin"])
        ET.SubElement(bndbox, "xmax").text = str(object["xmax"])
        ET.SubElement(bndbox, "ymax").text = str(object["ymax"])

    # create a new XML file with the results
    mydata = ET.tostring(root)

    xml_p = xml.dom.minidom.parseString(tostring(root))
    pretty_xml = xml_p.toprettyxml()

    return pretty_xml


def test():
    result = create_file_annotation(
        "test",
        "test.png",
        "/root/test/1233/test.png",
        (512, 1024, 3),
        [
            {
                "name": "verification_code",
                "pose": "Unspecified",
                "truncate": 0,
                "difficult": 0,
                "name": "name",
                "pose": "pose",
                "truncate": "truncate",
                "difficult": "difficult",
                "xmin": 0,
                "ymin": 0,
                "xmax": 512,
                "ymax": 1024,
            }
        ],
    )
    print(result)


if __name__ == "__main__":
    run_test = False
    if run_test:
        test()

    else:
        files_images = glob(
            "models/workspace/verification_code_train/images/test/**/**.png",
            recursive=True
            # "models/workspace/verification_code_train/images/**/**.png", recursive=True
        )
        amount_of_images = len(files_images)
        for i, image in enumerate(files_images[:]):
            print(f"{i}/{amount_of_images}")
            folder = abspath(image).split("/")[-2]
            file_path = abspath(image)
            _, ext = splitext(image)
            file_name = image.split("/")[-1]

            img = cv2.imread(image)
            size = img.shape
            size = (size[1], size[0], size[2])

            _, x1, y1, x2, y2, class_name = image.split(".")[0].split(";")
            xmin = int(x1)
            ymin = int(y1)
            xmax = xmin + int(x2)
            ymax = ymin + int(y2)

            xml_file = create_file_annotation(
                folder,
                file_name,
                file_path,
                size,
                [
                    {
                        "name": class_name,
                        "pose": "Unspecified",
                        "truncate": 0,
                        "difficult": 0,
                        "name": class_name,
                        "pose": "Unspecified",
                        "truncate": 0,
                        "difficult": 0,
                        "xmin": xmin,
                        "ymin": ymin,
                        "xmax": xmax,
                        "ymax": ymax,
                    }
                ],
            )
            open(file_path.replace(ext, ".xml"), "w").write(xml_file)

