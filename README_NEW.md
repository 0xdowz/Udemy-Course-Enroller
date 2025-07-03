# Udemy Course Enroller - أداة التسجيل في كورسات يودمي

**English** | [العربية](#arabic-section)

A comprehensive Python application that automatically discovers, filters, and enrolls in Udemy courses using coupon codes. Features a modern GUI with smart filtering, automated scheduling, and support for multiple course sources.

## 🔐 **Authentication Required**

**Important**: You must login first before using the application. The main interface will only open after successful authentication.

### Two Login Methods:
1. **Email/Password**: Login with your Udemy credentials
2. **Browser Session**: Use your existing browser session (auto-detected from available browsers)

## 🌟 Key Features

### 🎯 **Smart Course Discovery**
- Multi-source scraping (Real Discount, Discudemy)
- Intelligent filtering by rating, duration, language, and keywords
- Real-time course statistics and success tracking

### 🔐 **Secure Authentication**
- Email/password login support
- Browser cookie authentication (auto-detects available browsers)
- Intelligent default browser detection and prioritization
- Support for Chrome, Firefox, Edge, Safari, Brave, Opera, Opera GX
- Session validation and user verification

### 🎨 **Modern User Interface**
- Clean, professional design with dark/light theme toggle
- Responsive layout that adapts to different screen sizes
- Real-time feedback with progress indicators and status updates
- Debug mode for advanced users

### ⚡ **Automated Enrollment**
- Bulk enrollment with select all/none functionality
- Individual course enrollment options
- Rate limiting to respect server resources
- Comprehensive error handling and retry logic

### 📊 **Advanced Features**
- Course export to JSON format
- Sorting options (Recent, Rating, Duration, Title)
- Automated daily scheduling (9:00 AM)
- Desktop notifications for completed operations

## 🚀 Quick Start

### 1. Installation
```bash
git clone <repository-url>
cd udemy-course-enroller
pip install -r requirements.txt
```

### 2. Run Application
```bash
python main.py
```

### 3. Login Process
- The login window will appear first
- Choose your preferred login method:
  - **Email/Password**: Enter your Udemy credentials
  - **Browser Session**: Use existing Chrome session
- **The main interface will only open after successful login**

### 4. Using the Application
After successful login:
- Click "🔍 Discover Courses" to find available courses
- Use filters to narrow down results
- Select courses and click "⚡ Enroll" to enroll

## 📋 Requirements

- Python 3.7+
- Windows, macOS, or Linux
- One of the supported browsers (see Browser Support section)
- Active internet connection
- **Valid Udemy account credentials**

## 🌐 Browser Support

The application automatically detects and prioritizes browsers based on your system's default browser:

### Supported Browsers
- ✅ **Google Chrome** - All platforms
- ✅ **Mozilla Firefox** - All platforms
- ✅ **Microsoft Edge** - All platforms
- ✅ **Safari** - macOS only
- ✅ **Brave Browser** - All platforms
- ✅ **Opera** - All platforms
- ✅ **Opera GX** - All platforms

### Smart Browser Detection
- 🌟 **Default Browser Priority**: Your system's default browser is automatically detected and prioritized
- 🔍 **Auto-Detection**: Available browsers are automatically discovered
- 📊 **Smart Sorting**: Browsers are sorted by preference (default first, then by compatibility)
- ⚡ **One-Click Selection**: Choose from available browsers with visual indicators

### Browser Requirements
- You must be logged into Udemy in your chosen browser
- The browser must have stored cookies for udemy.com
- The application will show only available browsers with proper detection

### Alternative Login
If no supported browsers are available or cookie extraction fails, you can always use **email/password login** as a reliable alternative.

## 🔧 Installation Details

### Dependencies
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
browser-cookie3>=0.20.0
customtkinter>=5.2.0
schedule>=1.2.0
plyer>=2.1.0
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## 📖 Usage Guide

### Authentication Methods

#### Method 1: Email/Password Login
1. Launch the application: `python main.py`
2. In the login window, enter your Udemy email and password
3. Click "Sign In" button
4. Wait for authentication verification

#### Method 2: Browser Session Login
1. Make sure you're logged into Udemy in any supported browser
2. Launch the application: `python main.py`
3. The app will automatically detect your available browsers
4. Your default browser will be highlighted and prioritized
5. Choose your preferred browser from the available options
6. The app will use your browser session for authentication

### Main Interface Features

#### Course Discovery
- **Discover Button**: Fetch courses from multiple sources
- **Real-time Status**: See progress and operation status
- **Statistics Panel**: View total courses and filtering results

#### Smart Filtering
- **Rating Filter**: Set minimum course rating (0.0-5.0)
- **Duration Filter**: Set maximum course duration in hours
- **Language Filter**: Filter by course language
- **Keywords Filter**: Search for specific topics

#### Enrollment Options
- **Individual Enrollment**: Click "⚡ Enroll" on any course
- **Bulk Selection**: Use checkboxes to select multiple courses
- **Enroll Selected**: Enroll in all selected courses
- **Enroll All**: Enroll in all filtered courses

#### Advanced Features
- **Theme Toggle**: Switch between dark/light modes
- **Debug Mode**: Enable detailed logging and troubleshooting
- **Export Function**: Save course lists to JSON files
- **Sort Options**: Sort by recent, rating, duration, or title

## 🛠️ Troubleshooting

### Common Issues

#### "Authentication Failed"
- Verify your Udemy email and password are correct
- Ensure your Udemy account is not locked or suspended
- Try using browser session method instead

#### "Failed to load cookies from browser"
- Make sure you're logged into Udemy in your chosen browser
- Close your browser completely and restart it
- Try a different browser from the available options
- Use manual email/password login instead

#### "No courses found"
- Check your internet connection
- Verify source websites are accessible
- Try running the application later

#### "Enrollment failed"
- Verify you're not already enrolled in the course
- Check if the coupon is still valid
- Ensure your login session is still active

### Debug Mode
Enable debug mode by clicking the 🐛 button in the header to see detailed operation logs and troubleshooting information.

## 🔒 Security & Privacy

- Your credentials are processed locally and not stored
- Sessions are handled securely using standard authentication protocols
- No personal data is shared with third parties
- All operations respect Udemy's terms of service

## ⚖️ Legal & Ethical Use

- This tool is for educational purposes only
- Respect Udemy's terms of service
- Use reasonable delays to avoid server overload
- Only enroll in courses you genuinely intend to take

---

# <a id="arabic-section"></a>دليل الاستخدام باللغة العربية

## 🔐 **تسجيل الدخول مطلوب**

**مهم جداً**: يجب عليك تسجيل الدخول أولاً قبل استخدام الأداة. الواجهة الرئيسية لن تفتح إلا بعد المصادقة الناجحة.

### طريقتان لتسجيل الدخول:
1. **البريد الإلكتروني وكلمة المرور**: باستخدام بيانات حساب يودمي
2. **جلسة المتصفح**: استخدام أي متصفح مدعوم (كشف تلقائي للمتصفحات المتاحة)

## 🌟 الميزات الرئيسية

### 🎯 **اكتشاف ذكي للكورسات**
- البحث في مصادر متعددة (Real Discount, Discudemy)
- فلترة ذكية حسب التقييم والمدة واللغة والكلمات المفتاحية
- إحصائيات فورية ومتابعة معدل النجاح

### 🔐 **مصادقة آمنة**
- دعم تسجيل الدخول بالبريد وكلمة المرور
- مصادقة عبر ملفات تعريف ارتباط المتصفح (كشف تلقائي ذكي)
- كشف وإعطاء أولوية للمتصفح الافتراضي للمستخدم
- دعم Chrome, Firefox, Edge, Safari, Brave, Opera, Opera GX
- تحقق من الجلسة والمستخدم

### 🎨 **واجهة مستخدم حديثة**
- تصميم نظيف ومهني مع إمكانية التبديل بين الوضع المظلم والفاتح
- تخطيط متجاوب يتكيف مع أحجام الشاشات المختلفة
- تغذية راجعة فورية مع مؤشرات التقدم وتحديثات الحالة
- وضع التطوير للمستخدمين المتقدمين

### ⚡ **تسجيل تلقائي**
- تسجيل جماعي مع وظيفة تحديد الكل/عدم التحديد
- خيارات تسجيل فردية للكورسات
- حد معدل الطلبات لاحترام موارد الخادم
- معالجة شاملة للأخطاء ومنطق إعادة المحاولة

## 🚀 البدء السريع

### 1. التثبيت
```bash
git clone <repository-url>
cd udemy-course-enroller
pip install -r requirements.txt
```

### 2. تشغيل التطبيق
```bash
python main.py
```

### 3. عملية تسجيل الدخول
- ستظهر نافذة تسجيل الدخول أولاً
- اختر طريقة تسجيل الدخول المفضلة:
  - **البريد/كلمة المرور**: أدخل بيانات حساب يودمي
  - **جلسة المتصفح**: استخدم جلسة Chrome الحالية
- **الواجهة الرئيسية ستفتح فقط بعد تسجيل الدخول بنجاح**

### 4. استخدام التطبيق
بعد تسجيل الدخول بنجاح:
- اضغط "🔍 Discover Courses" لإيجاد الكورسات المتاحة
- استخدم الفلاتر لتضييق النتائج
- حدد الكورسات واضغط "⚡ Enroll" للتسجيل

## 🌐 دعم المتصفحات

التطبيق يكتشف ويعطي أولوية للمتصفحات تلقائياً بناءً على المتصفح الافتراضي للنظام:

### المتصفحات المدعومة
- ✅ **Google Chrome** - جميع الأنظمة
- ✅ **Mozilla Firefox** - جميع الأنظمة  
- ✅ **Microsoft Edge** - جميع الأنظمة
- ✅ **Safari** - macOS فقط
- ✅ **Brave Browser** - جميع الأنظمة
- ✅ **Opera** - جميع الأنظمة
- ✅ **Opera GX** - جميع الأنظمة

### كشف ذكي للمتصفحات
- 🌟 **أولوية المتصفح الافتراضي**: يتم كشف وإعطاء الأولوية للمتصفح الافتراضي تلقائياً
- 🔍 **كشف تلقائي**: اكتشاف المتصفحات المتاحة تلقائياً
- 📊 **ترتيب ذكي**: ترتيب المتصفحات حسب الأفضلية (الافتراضي أولاً، ثم حسب التوافق)
- ⚡ **اختيار بنقرة واحدة**: اختيار من المتصفحات المتاحة مع مؤشرات بصرية

### متطلبات المتصفح
- يجب أن تكون مسجل الدخول في يودمي في متصفحك المختار
- يجب أن يحتوي المتصفح على ملفات تعريف ارتباط محفوظة لـ udemy.com
- التطبيق سيُظهر فقط المتصفحات المتاحة مع الكشف الصحيح

### بديل تسجيل الدخول
إذا لم تكن هناك متصفحات مدعومة متاحة أو فشل استخراج ملفات تعريف الارتباط، يمكنك دائماً استخدام **تسجيل الدخول بالبريد وكلمة المرور** كبديل موثوق.

## 🛠️ حل المشاكل الشائعة

### ❌ "فشل في المصادقة"
- تحقق من صحة بريدك الإلكتروني وكلمة المرور في يودمي
- تأكد من أن حساب يودمي غير مقفل أو معلق
- جرب استخدام طريقة جلسة المتصفح

### ❌ "فشل في تحميل ملفات تعريف الارتباط من المتصفح"
- تأكد من أنك مسجل الدخول في يودمي في المتصفح المختار
- أغلق المتصفح تماماً وأعد تشغيله
- جرب متصفحاً آخر من الخيارات المتاحة
- استخدم تسجيل الدخول اليدوي بالبريد وكلمة المرور

### ❌ "لا توجد كورسات"
- تحقق من اتصالك بالإنترنت
- تأكد من أن مواقع المصادر متاحة
- جرب تشغيل التطبيق لاحقاً

### ❌ "فشل التسجيل"
- تحقق من أنك لم تسجل في الكورس من قبل
- تأكد من أن الكوبون ما زال صالحاً
- تأكد من أن جلسة تسجيل الدخول ما زالت نشطة

## 🔒 الأمان والخصوصية

- بياناتك تتم معالجتها محلياً ولا يتم حفظها
- الجلسات تتم معالجتها بأمان باستخدام بروتوكولات المصادقة المعيارية
- لا يتم مشاركة البيانات الشخصية مع أطراف ثالثة
- جميع العمليات تحترم شروط خدمة يودمي

## ⚖️ الاستخدام القانوني والأخلاقي

- هذه الأداة للأغراض التعليمية فقط
- احترم شروط خدمة يودمي
- استخدم تأخيرات معقولة لتجنب إرهاق الخادم
- سجل فقط في الكورسات التي تنوي حقاً أخذها

---

## 📞 الدعم

للحصول على الدعم أو الإبلاغ عن المشاكل:
1. فعل وضع التطوير لرؤية تفاصيل الأخطاء
2. تحقق من ملف السجل `udemy_enroller.log`
3. أعد تشغيل التطبيق

**تذكر**: تسجيل الدخول مطلوب قبل استخدام أي ميزة في التطبيق! 🔐
