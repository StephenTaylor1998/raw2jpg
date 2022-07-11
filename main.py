import os

script = """run("Raw...", "open={} image=[{}] width={} height={} offset={}");
saveAs("{}", "{}");
close();
"""

image_type_dict = dict(
    png="PNG",
    jpg="Jpeg"
)


def generate_script(
        raw_path: str,
        raw_width: int,
        raw_height: int,
        offset: int,
        out_path: str = None,
        out_type: str = "PNG",
        data_type: str = "16-bit Signed"
):
    return script.format(raw_path, data_type, raw_width, raw_height, offset, out_type, out_path)


def read_xxx_file_info(xxx_file_path: str):
    with open(xxx_file_path, "rb") as f:
        lines = str(f.read(512)).split(r"\n")

    width = int(lines[4].split(r"\t")[-1])
    height = int(lines[5].split(r"\t")[-1])
    return height, width


def process_raw_in_dir(root_path: str, out_path: str, offset: int, image_type="jpg"):
    file_list = os.listdir(root_path)
    script_list = []
    for file_name in file_list:
        input_path = os.path.join(root_path, file_name)
        output_path = os.path.join(out_path, file_name[:-3] + image_type)
        height, width = read_xxx_file_info(input_path)
        imagej_script = generate_script(
            input_path, height, width, offset,
            output_path, image_type_dict[image_type]
        )
        script_list.append(imagej_script)

    return script_list


script_list = process_raw_in_dir(
    root_path="./raw_image",
    out_path="./output",
    offset=4096,
    image_type="jpg"
)

for sc in script_list:
    print(sc)

with open("raw2png.ijm", "w") as f:
    f.writelines(script_list)
