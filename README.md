# Udemy Course Enroller

A professional Python application that automatically finds and enrolls in free Udemy courses using valid coupon codes. Designed with a modern GUI, smart filtering, and support for multiple browsers and sources.

## Table of Contents

- [Features](#features)
- [Authentication](#authentication)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Browser Support](#browser-support)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [Security & Privacy](#security--privacy)
- [Legal Notice](#legal-notice)
- [Support](#support)
- [Arabic Version](#arabic-version)

---

## Features

### Smart Course Discovery
- Multi-source scraping (Real Discount, Discudemy)
- Filtering by rating, language, duration, and keywords
- Displays real-time statistics and course metadata

### Secure Authentication
- Email/password login
- Cookie-based authentication from existing browser sessions
- Auto-detection and prioritization of the default browser

### Modern GUI
- Clean interface with light/dark theme toggle
- Real-time status updates and progress indicators
- Debug mode for advanced users

### Automated Enrollment
- Bulk or individual course enrollment
- Automatic rate limiting
- Error handling and retry logic

### Advanced Utilities
- Daily auto-scheduling at 9:00 AM
- Export courses to JSON
- Sorting by rating, date, duration, or title
- Desktop notifications

---

## Authentication

Before using the application, you must log in. The main interface becomes accessible only after a successful login.

### Login Options
1. Email and password
2. Browser session cookies (Chrome, Firefox, etc.)

---

## Quick Start

### 1. Clone and Install
```bash
git clone https://github.com/0xdowz/udemy-course-enroller.git
cd udemy-course-enroller
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

### 3. Login Process
- Choose your preferred login method
- After successful login, access the full GUI

---

## Requirements

- Python 3.7 or higher
- Windows, macOS, or Linux
- Active internet connection
- A valid Udemy account
- A supported browser (for cookie-based login)

---

## Browser Support

Supported browsers for session authentication:

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Safari (macOS only)
- Brave
- Opera / Opera GX

The application auto-detects available browsers and selects the default system browser if available.

---

## Usage Guide

### Discovering Courses
- Click "Discover Courses" to fetch available coupons
- Apply filters (rating, language, duration, keywords)
- Sort results and view statistics

### Enrolling
- Select courses individually or in bulk
- Click "Enroll" to register in selected courses

### Export & Schedule
- Export course list as JSON
- Set up automatic daily enrollment at 9:00 AM

---

## Troubleshooting

**Authentication failed**  
- Verify your email and password  
- Try switching to browser session login  

**Cookies not loaded**  
- Ensure you're logged into Udemy in the selected browser  
- Restart the browser and try again  

**No courses found**  
- Check internet connection  
- Wait and retry; sources may be temporarily down  

**Enrollment failed**  
- You may already be enrolled  
- Coupon may have expired  
- Your session may have expired

---

## Security & Privacy

- No credentials are stored; all authentication is handled locally
- Sessions use secure and standard mechanisms
- No data is shared with third parties
- Complies with Udemy's terms of service

---

## Legal Notice

This tool is for educational use only.  
Always respect Udemy’s terms of service.  
Do not abuse coupon usage or overwhelm servers.

---

## Support

To report issues or contribute, please open an [issue](https://github.com/your-username/udemy-course-enroller/issues) or submit a [pull request](https://github.com/your-username/udemy-course-enroller/pulls).

---

# Arabic Version

## نظرة عامة

أداة بايثون ذكية تتيح لك اكتشاف والتسجيل في كورسات Udemy المجانية باستخدام كوبونات فعالة، مع واجهة رسومية احترافية ونظام فلترة متقدم، ودعم للمتصفحات المتعددة.

## المزايا

### اكتشاف ذكي للكورسات
- البحث في مصادر متعددة مثل Real Discount و Discudemy
- فلترة حسب التقييم واللغة والمدة والكلمات المفتاحية
- إحصائيات فورية وعرض بيانات الكورس

### تسجيل دخول آمن
- تسجيل الدخول باستخدام البريد وكلمة المرور
- استخدام ملفات تعريف الارتباط من متصفحك الحالي
- كشف وتحديد المتصفح الافتراضي تلقائيًا

### واجهة مستخدم حديثة
- تصميم نظيف مع إمكانية التبديل بين الوضع الفاتح والمظلم
- تحديثات فورية لحالة العمليات
- وضع Debug للمستخدمين المتقدمين

### تسجيل تلقائي ذكي
- تسجيل فردي أو جماعي في الكورسات
- احترام معدل الطلبات وتفادي الحظر
- منطق شامل للتعامل مع الأخطاء

### أدوات متقدمة
- جدولة تلقائية يومية الساعة 9:00 صباحًا
- تصدير قائمة الكورسات إلى JSON
- فرز النتائج بالتقييم أو العنوان أو المدة أو التاريخ
- إشعارات على سطح المكتب بعد انتهاء العمليات

---

## طريقة الاستخدام

1. قم بتثبيت المتطلبات وتشغيل التطبيق
2. سجّل الدخول باستخدام الطريقة المناسبة
3. استخدم زر "اكتشاف الكورسات" للبحث
4. طبّق الفلاتر، ثم سجل في الكورسات التي ترغب بها

---

## متطلبات النظام

- Python 3.7 أو أحدث
- نظام تشغيل Windows أو macOS أو Linux
- اتصال بالإنترنت
- حساب يودمي صالح
- متصفح مدعوم

---

## المتصفحات المدعومة

- Google Chrome  
- Mozilla Firefox  
- Microsoft Edge  
- Safari (macOS فقط)  
- Brave  
- Opera / Opera GX  

يقوم التطبيق بكشف المتصفح الافتراضي تلقائيًا، ويمكنك اختيار متصفح آخر يدويًا إذا أردت.

---

## استكشاف الأخطاء

**فشل تسجيل الدخول**  
- تحقق من صحة بياناتك  
- جرّب استخدام طريقة الجلسة من المتصفح

**فشل تحميل ملفات تعريف الارتباط**  
- تأكد من تسجيل الدخول في المتصفح  
- أعد تشغيل المتصفح أو جرّب متصفحًا آخر

**لا توجد كورسات**  
- تأكد من اتصالك بالإنترنت  
- المصادر قد تكون غير متاحة مؤقتًا

**فشل التسجيل**  
- قد تكون مُسجل بالفعل  
- تأكد من أن الكوبون لا يزال صالحًا  
- تحقق من أن الجلسة لا تزال نشطة

---

## الأمان والخصوصية

- لا يتم حفظ أي بيانات حساسة
- تتم جميع عمليات المصادقة محليًا وبشكل آمن
- لا يتم مشاركة أي بيانات مع طرف ثالث
- الأداة ملتزمة بشروط خدمة يودمي

---

## الاستخدام القانوني

- هذه الأداة مخصصة للأغراض التعليمية فقط  
- لا تسيء استخدامها أو تسجل في كورسات لا تنوي متابعتها  
- احترم شروط خدمة Udemy دائمًا

---
