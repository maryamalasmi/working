# مشروع التعلم الفيدرالي المنيع ضد هجمات التسمم (Federated Learning Security)

هذا الملف يشرح كيفية إعداد البيئة البرمجية للمشروع خطوة بخطوة على نظام **Ubuntu Linux**.

---

## 1. تثبيت الحزم الأساسية للنظام
افتحي الـ Terminal في أوبونتو ونفذي الأمر التالي:

```bash
sudo apt update && sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential git






# الانتقال إلى المجلد الرئيسي وإنشاء مجلد المشروع
cd ~
mkdir federated_project
cd federated_project

# إنشاء البيئة الافتراضية وتفعيلها
python3 -m venv fl_env
source fl_env/bin/activate





pip install --upgrade pip
pip install tensorflow numpy scipy matplotlib pandas





import tensorflow as tf
import numpy as np
import scipy
import matplotlib
import pandas as pd

print("جميع المكتبات تعمل بنجاح!")
print(f"TensorFlow Version: {tf.__version__}")