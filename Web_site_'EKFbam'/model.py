from ultralytics import YOLO
from math import sqrt

import cv2, easyocr


# Увеличение изображения
def improve_image(image_name, image_format):    
    image = cv2.imread(f'static/image_analysis/first_image/{image_name}.{image_format}') 
     
    scaled_image = cv2.resize(image, None, fx=2, fy=2) 
    
    cv2.imwrite(f'static/image_analysis/improve_image/{image_name}.{image_format}', scaled_image) 
    
    return {
        'status': 200,
        'message': 'Успешная обработка',
        'path_result': f'static/image_analysis/improve_image/{image_name}.{image_format}'
    }
    
# Инференс модели по объектам в формате картинки
def inferens_yolo_img(image_name, image_format):
    model = YOLO('models/378epN.pt')
    
    results = model.predict(f'static/image_analysis/improve_image/{image_name}.{image_format}')
    
    for result in results:
        result.save(filename=f'static/image_analysis/result_object_image/{image_name}.{image_format}')
    
    return {
        'status': 200,
        'message': 'Успешная обработка',
        'path_result': f'static/image_analysis/result_object_image/{image_name}.{image_format}'
    }

# Инференс модели по объектам
def inferens_yolo(image_name, image_format):
    model = YOLO('models/EKFbam-350ep.pt')
    
    results = model.predict(f'static/image_analysis/improve_image/{image_name}.{image_format}')
    
    list_object = list()
    list_coordination_object = list()
        
    for result in results:
        for index in range(len(result.boxes.cls)):
            list_object.append(int(result.boxes.cls[index].tolist()))
            list_coordination_object.append(result.boxes.xyxy[index].tolist())
    
    return list_object, list_coordination_object

# Инференс модели по тексту
def inferens_text(image_name, image_format, x1, y1, x2, y2):
    reader = easyocr.Reader(['ru','en'], gpu=True)
    img = cv2.imread(f'static/image_analysis/improve_image/{image_name}.{image_format}')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    roi = img[y1:y2, x1:x2]
    results = reader.readtext(roi, detail = 0)
    
    return results

# Функция вычисления наиближайшего текста к объекту
def are_objects_close(x1, y1, x2, y2, x3, y3, x4, y4):
    center1_x = (x1 + x2) / 2
    center1_y = (y1 + y2) / 2
    center2_x = (x3 + x4) / 2
    center2_y = (y3 + y4) / 2
    
    distance = sqrt((center1_x - center2_x)**2 + (center1_y - center2_y)**2)
    
    return distance

# Составление ответа для модуля compilation
def inferens(image_name, image_format):
    list_object, list_coordination_object = inferens_yolo(image_name, image_format)
    
    object_classes = ['Текст', "QF", 'QS', 'Шкаф', 'WH', 'TT', 'KM', 'AVR', 'FU', 'K', 'HL', 'switch', 'PA', 'PV', 'QFD', 'QFU', 'FV', 'OPS', 'ITU', 'S', 'AUX', 'M', 'R', 'YZIP', 'QW', 'XS', 'MX', 'Q', 'PM', 'SB', 'FR', 'QD', 'U<', 'Timer']
    
    result = list()
    result_list = list()
    list_text = list()
    
    for index in range(len(list_object)):
        if list_object[index] != 0:
            result_list.append([str(object_classes[list_object[index]])]+[index])
        else:
            x1 = int(list_coordination_object[index][0])
            y1 = int(list_coordination_object[index][1])
            x2 = int(list_coordination_object[index][2])
            y2 = int(list_coordination_object[index][3])
            list_text.append(inferens_text(image_name, image_format, x1, y1, x2, y2)+[index])
            
    list_help = []
    list_help_1 = []
    
    for index_list in range(len(result_list)):
        coord_obj = list_coordination_object[result_list[index_list][1]]
        obj_1_x1 = coord_obj[0]
        obj_1_y1 = coord_obj[1]
        obj_1_x2 = coord_obj[2]
        obj_1_y2 = coord_obj[3]
        for index_text in range(len(list_text)):
            coord_text = list_coordination_object[list_text[index_text][-1]]
            obj_2_x1 = coord_text[0]
            obj_2_y1 = coord_text[1]
            obj_2_x2 = coord_text[2]
            obj_2_y2 = coord_text[3]
            list_help.append(are_objects_close(obj_1_x1, obj_1_y1, obj_1_x2, obj_1_y2, obj_2_x1, obj_2_y1, obj_2_x2, obj_2_y2))
            list_help_1.append(list_text[index_text])
        del result_list[index_list][-1]
        result_list[index_list] += [list_help_1[list_help.index(min(list_help))]]
        list_help = []
        list_help_1 = []
    
    for index_list_1 in range(len(result_list)):
        if isinstance(result_list[index_list_1][1][-1], int):
            del result_list[index_list_1][1][-1]
        
    for item in result_list:
        first_element = item[0]
        
        second_element = ';'.join([str(x) for x in item[1]])
        
        result.append([first_element, second_element])
    
    return {
        'status_inferens': True,
        'objects': result,
        'name_file': image_name
    }
