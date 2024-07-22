from collections import defaultdict

import xml.etree.ElementTree as ET
import os, shutil

def create_classes(file_data):
    tree = ET.parse(f'{file_data}/annotations.xml')
    root = tree.getroot()

    file = open('classes.txt', 'r', encoding='utf-8')
    classes = list()
    classes = [line.strip() for line in file]
    classes_add = list()
    file.close()
    print(classes)
    for box in root.findall('image/box'):
        label = box.get('label')
        if label not in classes and label not in classes_add:
            classes_add.append(label)
    file = open("classes.txt", "a", encoding='utf-8')
    
    for object in classes_add:
        file.write(object)
        file.write('\n')
    file.close()

def convert_yolo_xywh(x0, y0, x1, y1, image_width, image_height):
    x = (x0 + x1) / (2 * image_width)
    y = (y0 + y1) / (2 * image_height)
    w = (x1 - x0) / image_width
    h = (y1 - y0) / image_height
    
    return str(x), str(y), str(w), str(h)


def add_txt(file, path_file, path_data):
    file_name = file[4:len(file)-4]
    file_txt = open(f'{path_file}/{file_name}.txt', 'w+', encoding='utf-8')

    tree = ET.parse(f'{path_data}/annotations.xml')
    root = tree.getroot()

    file_classes = open('classes.txt', 'r', encoding='utf-8')
    classes = list()
    classes = [line.strip() for line in file_classes]
    file_classes.close()
    # Ищем элемент с name="EKF/1-page-00001.jpg"
    for image in root.findall('image'):
        if image.get('name') == file:
            # Выводим значения label для всех box-элементов в этом image
            for box in image.findall('box'):
                object = box.get('label')
                for index in range(len(classes)):
                    if object == classes[index]:
                        file_txt.write(str(index))
                        break
                # сделать добавление индекса а не самого названия
                x, y, w, h = convert_yolo_xywh(float(box.get('xtl')), float(box.get('ytl')), float(box.get('xbr')), float(box.get('ybr')), int(image.get('width')), int(image.get('height')))
                file_txt.write(' ')
                file_txt.write(x + ('0' * (8 - len(x))))
                file_txt.write(' ')
                file_txt.write(y + ('0' * (8 - len(y))))
                file_txt.write(' ')
                file_txt.write(w + ('0' * (8 - len(w))))
                file_txt.write(' ')
                file_txt.write(h + ('0' * (8 - len(h))))
                file_txt.write('\n')
    file_txt.close()
    
def work_file(file, path_file, path_data):
    file_name = file[4:]
    shutil.move(f"{path_file}/images/{file}", f"{path_data}/{file_name}")
    add_txt(file, path_data, path_file)
    
def create_data(file_data, path_data):
    tree = ET.parse(f'{file_data}/annotations.xml')
    root = tree.getroot()

    file = open('help_file.txt', 'r', encoding='utf-8')
    
    image_list = list()
    image_list = [line.strip() for line in file]
    file.close()
    for image in root.findall('image'):
        label = image.get('name')
        if label not in image_list:
            image_list.append(label)
            print(label, file_data, path_data)
            work_file(label, file_data, path_data)      
            
    file = open("help_file.txt", "a", encoding='utf-8')
    
    for image in image_list:
        file.write(image)
        file.write('\n')
    file.close()

def train_val_yolo(source_dir, dest_dir):
    file_counts = defaultdict(int)
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_path):
            file_count = file_counts[filename]
            if file_count > 0:
                dest_filename = f"{os.path.splitext(filename)[0]}_{file_count}{os.path.splitext(filename)[1]}"
            else:
                dest_filename = filename
            dest_path = os.path.join(dest_dir, dest_filename)
            shutil.move(source_path, dest_path)
            file_counts[filename] += 1

def trva():
    source_folder = 'my_dataset/images/train'

    # Укажи путь к папке, куда нужно переместить файлы
    destination_folder = 'my_dataset/images/val'

    # Создаем список файлов в исходной папке
    files = os.listdir(source_folder)

    # Перемещаем первые 40 файлов
    for i, file in enumerate(files):
        if i < 400:
            source_path = os.path.join(source_folder, file)
            destination_path = os.path.join(destination_folder, file)
            shutil.move(source_path, destination_path)
            print(f'Переместил файл: {file}')
        else:
            break

def lbtrva():
    source_dir = 'my_dataset/images/train'

    destination_dir = 'my_dataset/labels/train'

    if not os.path.exists(source_dir):
        print(f"Папка {source_dir} не существует.")
        exit()

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Папка {destination_dir} была создана.")

    for filename in os.listdir(source_dir):
        if filename.endswith(".txt"):
            source_file = os.path.join(source_dir, filename)
            destination_file = os.path.join(destination_dir, filename)
            
            shutil.move(source_file, destination_file)
            print(f"Файл {filename} перемещен.")

    print("Все файлы .txt перемещены в train")

    source_dir = 'my_dataset/images/val'

    destination_dir = 'my_dataset/labels/val'

    if not os.path.exists(source_dir):
        print(f"Папка {source_dir} не существует.")
        exit()

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Папка {destination_dir} была создана.")

    for filename in os.listdir(source_dir):
        if filename.endswith(".txt"):
            source_file = os.path.join(source_dir, filename)
            destination_file = os.path.join(destination_dir, filename)
            
            shutil.move(source_file, destination_file)
            print(f"Файл {filename} перемещен.")

    print("Все файлы .txt перемещены в val")
    
if __name__ == '__main__':
    paths = ['330', '331', '333', '334', '482']
    paths_data = ['data_for_yolo_330', 'data_for_yolo_331', 'data_for_yolo_333', 'data_for_yolo_334', 'data_for_yolo_482']
    os.mkdir('data_for_yolo_330')
    os.mkdir('data_for_yolo_331')
    os.mkdir('data_for_yolo_333')
    os.mkdir('data_for_yolo_334')
    os.mkdir('data_for_yolo_482')
    for file in paths:
        create_classes(file)
    for file in range(len(paths)):
        create_data(paths[file], paths_data[file])
    os.mkdir('my_dataset')
    os.mkdir('my_dataset/images')
    os.mkdir('my_dataset/images/train')
    os.mkdir('my_dataset/images/val')
    for path in paths_data:
        train_val_yolo(path, 'my_dataset/images/train')
    trva()
    os.mkdir('my_dataset/labels')
    os.mkdir('my_dataset/labels/train')
    os.mkdir('my_dataset/labels/val')
    lbtrva()
    shutil.rmtree("330")
    shutil.rmtree("331")
    shutil.rmtree("333")
    shutil.rmtree("334")
    shutil.rmtree("482")
    shutil.rmtree("data_for_yolo_330")
    shutil.rmtree("data_for_yolo_331")
    shutil.rmtree("data_for_yolo_333")
    shutil.rmtree("data_for_yolo_334")
    shutil.rmtree("data_for_yolo_482")