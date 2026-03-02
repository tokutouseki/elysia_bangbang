#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import argparse
import numpy as np
import onnxruntime as ort

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# 默认模型文件路径（当前目录下的best.onnx）
default_model_path = os.path.join(script_dir, "best.onnx")

"""
================================================================================
                        YOLO 模型预测工具使用说明
================================================================================

【基本用法】
    python predict.py --img "图片路径" --model "模型路径"

【常用参数】
    --img        图片文件路径（必需）
    --model      模型文件路径（可选，默认: 当前目录下的best.onnx）
    --conf       置信度阈值（可选，默认: 0.25）
    --save       是否保存结果图片（可选，默认: False）
    --show       是否显示结果图片（可选，默认: False）

【使用示例】

1. 基本预测（使用默认模型）:
   python predict.py --img "test.jpg"

2. 指定模型:
   python predict.py --img "test.jpg" --model "models/yolov10n.onnx"

3. 调整置信度阈值:
   python predict.py --img "test.jpg" --conf 0.5

4. 保存结果图片:
   python predict.py --img "test.jpg" --save True

5. 显示结果图片:
   python predict.py --img "test.jpg" --show True

【输出说明】
    - 识别结果将以JSON格式输出
    - 每个检测结果包含：类别ID、标签名称、置信度、边界框坐标
    - 边界框坐标格式：[x1, y1, x2, y2]（左上角和右下角坐标）

【注意事项】
    - 确保模型文件路径正确
    - 支持常见图片格式：jpg, jpeg, png, bmp等
    - 置信度阈值范围：0-1，值越大识别越严格

================================================================================
"""

# 类别名称映射
CLASS_NAMES = {
    0: 'elysia_star',
    1: 'aomie',
    2: 'zhenwo',
    3: 'kongmeng',
    4: 'shanbiyvjing',
    5: 'xuanze_R',
    6: 'guaiwu_xueliang_UI',
    7: 'xuanze_r',
    8: 'keyin',
    9: 'keyin_open',
    10: 'shangdian',
    11: 'jielv',
    12: 'luoxuan',
    13: 'shangdian_open',
    14: 'tianhui',
    15: 'fanxing',
    16: 'lock_on',
    17: 'wuxian',
    18: 'chana',
    19: 'huangjin',
    20: 'jiushi',
    21: 'xvguang',
    22: 'fusheng',
    23: 'BOSS'
}

def preprocess_image(image, target_size=(640, 640)):
    """
    预处理图片
    
    :param image: 输入图片（OpenCV格式）
    :param target_size: 目标尺寸
    :return: 预处理后的输入数据
    """
    # 保存原始尺寸
    h, w = image.shape[:2]
    
    # 调整图片大小
    img = cv2.resize(image, target_size)
    
    # 转换为RGB格式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 归一化处理
    img = img.astype(np.float32) / 255.0
    
    # 调整维度顺序 (H, W, C) -> (C, H, W)
    img = np.transpose(img, (2, 0, 1))
    
    # 添加批次维度
    img = np.expand_dims(img, axis=0)
    
    return img, h, w

def postprocess_output(output, conf_threshold=0.25, input_size=(384, 640), original_size=None):
    """
    后处理输出结果
    
    :param output: ONNX模型输出
    :param conf_threshold: 置信度阈值
    :param input_size: 模型输入尺寸
    :param original_size: 原始图片尺寸
    :return: 处理后的预测结果
    """
    predictions = []
    
    # 获取输出数据
    output_data = output[0][0]  # 去除批次维度，得到 (300, 6) 的检测结果
    
    # 处理每个检测结果
    for detection in output_data:
        x1, y1, x2, y2, confidence, class_id = detection
        
        # 过滤低置信度结果
        if confidence < conf_threshold:
            continue
        
        # 转换为整数
        class_id = int(class_id)
        
        # 获取类别名称
        class_name = CLASS_NAMES.get(class_id, f"class_{class_id}")
        
        # 坐标转换（如果提供了原始尺寸）
        if original_size:
            orig_h, orig_w = original_size
            input_h, input_w = input_size
            
            # 计算缩放比例
            scale_x = orig_w / input_w
            scale_y = orig_h / input_h
            
            # 调整边界框坐标
            x1 = x1 * scale_x
            y1 = y1 * scale_y
            x2 = x2 * scale_x
            y2 = y2 * scale_y
        
        # 添加到结果列表
        predictions.append({
            "class_id": class_id,
            "class_name": class_name,
            "confidence": float(confidence),
            "bbox": [float(x1), float(y1), float(x2), float(y2)]
        })
    
    # 按置信度排序
    predictions.sort(key=lambda x: x["confidence"], reverse=True)
    
    return predictions

def predict_image(
    image_path,
    model_path=default_model_path,
    conf_threshold=0.25,
    save_result=False,
    show_result=False
):
    """
    使用ONNX模型预测图片
    
    :param image_path: 图片文件路径
    :param model_path: 模型文件路径
    :param conf_threshold: 置信度阈值
    :param save_result: 是否保存结果图片
    :param show_result: 是否显示结果图片
    :return: 预测结果列表
    """
    # 检查图片文件是否存在
    if not os.path.exists(image_path):
        print(f"错误: 图片文件 '{image_path}' 不存在")
        return None
    
    # 检查模型文件是否存在
    if not os.path.exists(model_path):
        print(f"错误: 模型文件 '{model_path}' 不存在")
        return None
    
    # 加载模型
    try:
        # 尝试使用GPU执行提供者
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        session = ort.InferenceSession(model_path, providers=providers)
        # 检查实际使用的执行提供者
        used_providers = session.get_providers()
        print(f"✅ ONNX模型加载成功")
        print(f"   执行提供者: {used_providers}")
    except Exception as e:
        print(f"❌ 加载ONNX模型失败: {e}")
        return None
    
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"错误: 无法读取图片 '{image_path}'")
        return None
    
    # 预处理图片
    input_data, orig_h, orig_w = preprocess_image(image)
    
    # 获取输入名称
    input_name = session.get_inputs()[0].name
    
    # 进行推理
    try:
        outputs = session.run(None, {input_name: input_data})
    except Exception as e:
        print(f"❌ 推理失败: {e}")
        return None
    
    # 后处理输出
    predictions = postprocess_output(
        outputs,
        conf_threshold=conf_threshold,
        input_size=(640, 640),
        original_size=(orig_h, orig_w)
    )
    
    # 绘制结果
    if save_result or show_result:
        result_image = image.copy()
        
        # 绘制边界框和标签
        for pred in predictions:
            x1, y1, x2, y2 = pred["bbox"]
            class_name = pred["class_name"]
            confidence = pred["confidence"]
            
            # 绘制边界框
            cv2.rectangle(result_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            
            # 绘制标签
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(result_image, label, (int(x1), int(y1) - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # 保存结果图片
        if save_result:
            # 创建结果目录
            save_dir = os.path.join(os.path.dirname(model_path), "predict_results")
            os.makedirs(save_dir, exist_ok=True)
            
            # 保存图片
            img_name = os.path.basename(image_path)
            save_path = os.path.join(save_dir, f"result_{img_name}")
            cv2.imwrite(save_path, result_image)
            print(f"结果图片已保存到: {save_path}")
        
        # 显示结果图片
        if show_result:
            cv2.imshow("YOLO Prediction", result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    return predictions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YOLO 模型预测工具')
    parser.add_argument('--img', type=str, required=True, help='图片文件路径')
    parser.add_argument('--model', type=str, default=default_model_path, help='模型文件路径')
    parser.add_argument('--conf', type=float, default=0.25, help='置信度阈值')
    parser.add_argument('--save', type=bool, default=False, help='是否保存结果图片')
    parser.add_argument('--show', type=bool, default=False, help='是否显示结果图片')
    parser.add_argument('--json', type=bool, default=False, help='是否以JSON格式输出结果')
    
    args = parser.parse_args()
    
    # 执行预测
    predictions = predict_image(
        image_path=args.img,
        model_path=args.model,
        conf_threshold=args.conf,
        save_result=args.save,
        show_result=args.show
    )
    
    # 输出结果
    if predictions:
        if args.json:
            # 以JSON格式输出
            import json
            output_data = {
                "success": True,
                "total_objects": len(predictions),
                "predictions": predictions
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
        else:
            # 以普通文本格式输出
            print("\n" + "=" * 60)
            print("预测结果")
            print("=" * 60)
            print(f"识别到 {len(predictions)} 个目标")
            print("=" * 60)
            
            for i, pred in enumerate(predictions, 1):
                print(f"\n目标 {i}:")
                print(f"  类别ID: {pred['class_id']}")
                print(f"  类别名称: {pred['class_name']}")
                print(f"  置信度: {pred['confidence']:.4f}")
                print(f"  边界框坐标: {pred['bbox']}")
                print(f"    - 左上角: ({pred['bbox'][0]:.2f}, {pred['bbox'][1]:.2f})")
                print(f"    - 右下角: ({pred['bbox'][2]:.2f}, {pred['bbox'][3]:.2f})")
            
            print("\n" + "=" * 60)
    else:
        if args.json:
            # 以JSON格式输出失败信息
            import json
            output_data = {
                "success": False,
                "message": "预测失败"
            }
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
        else:
            print("预测失败")