# Browser Support Guide - دليل دعم المتصفحات

## English

### Supported Browsers

The Udemy Course Enroller supports cookie-based authentication from multiple browsers with intelligent default browser detection:

#### ✅ **Google Chrome**
- **Platforms**: Windows, macOS, Linux
- **Requirements**: Must be logged into Udemy
- **Detection**: Automatic detection of Chrome installation and user data

#### ✅ **Mozilla Firefox**
- **Platforms**: Windows, macOS, Linux
- **Requirements**: Must be logged into Udemy
- **Detection**: Automatic detection of Firefox profiles and cookies

#### ✅ **Microsoft Edge**
- **Platforms**: Windows, macOS, Linux
- **Requirements**: Must be logged into Udemy
- **Detection**: Automatic detection of Edge installation and user data

#### ✅ **Safari**
- **Platforms**: macOS only
- **Requirements**: Must be logged into Udemy
- **Detection**: Automatic detection of Safari cookies (macOS only)

#### ✅ **Brave Browser**
- **Platforms**: Windows, macOS, Linux
- **Requirements**: Must be logged into Udemy
- **Detection**: Automatic detection of Brave installation and user data
- **Note**: Uses Chrome-based cookie format

#### ✅ **Opera**
- **Platforms**: Windows, macOS, Linux
- **Requirements**: Must be logged into Udemy
- **Detection**: Automatic detection of Opera installation and user data

#### ✅ **Opera GX**
- **Platforms**: Windows, macOS, Linux
- **Requirements**: Must be logged into Udemy
- **Detection**: Automatic detection of Opera GX installation and user data
- **Note**: Gaming-focused version of Opera

### How Browser Detection Works

1. **Default Browser Detection**: The application first detects your system's default browser
2. **Automatic Discovery**: Scans your system for installed supported browsers
3. **Smart Prioritization**: Orders browsers with your default browser first, then by compatibility
4. **Cookie Validation**: Checks if each browser has valid Udemy cookies
5. **Dynamic UI**: Shows only available browsers in the login window with visual indicators
6. **Fallback Support**: If no browsers are detected, email/password login is still available

### Browser Selection Process

1. **Default Browser Priority**: If your default browser is detected and available, it's highlighted and recommended
2. **Multiple Browsers**: If multiple browsers are available, they're sorted by preference (default first)
3. **Visual Indicators**: Default browser is marked with 🌟 and uses different colors
4. **Single Browser**: If only one browser is available, it's selected automatically
5. **No Browsers**: If no browsers are available, only email/password login is shown

### Troubleshooting Browser Issues

#### "No supported browsers found"
- Install one of the supported browsers
- Make sure you're logged into Udemy in that browser
- Use email/password login as an alternative

#### "Failed to load cookies from [Browser]"
- Ensure you're logged into Udemy in the selected browser
- Close and restart the browser
- Clear browser cache and log in again
- Try a different browser
- Use email/password login as an alternative

#### "Authentication failed"
- Check if your Udemy session is still active
- Log out and log back into Udemy in your browser
- Try using email/password login instead

### Best Practices

1. **Stay Logged In**: Keep your Udemy session active in your preferred browser
2. **Use Primary Browser**: Use the browser you normally use for web browsing
3. **Keep Cookies**: Don't clear cookies for udemy.com
4. **Backup Method**: Always remember that email/password login is available as a backup

---

## العربية

### المتصفحات المدعومة

أداة التسجيل في كورسات يودمي تدعم مصادقة ملفات تعريف الارتباط من متصفحات متعددة مع كشف ذكي للمتصفح الافتراضي:

#### ✅ **Google Chrome**
- **الأنظمة**: Windows, macOS, Linux
- **المتطلبات**: يجب أن تكون مسجل الدخول في يودمي
- **الكشف**: كشف تلقائي لتثبيت Chrome وبيانات المستخدم

#### ✅ **Mozilla Firefox**
- **الأنظمة**: Windows, macOS, Linux
- **المتطلبات**: يجب أن تكون مسجل الدخول في يودمي
- **الكشف**: كشف تلقائي لملفات تعريف Firefox وملفات تعريف الارتباط

#### ✅ **Microsoft Edge**
- **الأنظمة**: Windows, macOS, Linux
- **المتطلبات**: يجب أن تكون مسجل الدخول في يودمي
- **الكشف**: كشف تلقائي لتثبيت Edge وبيانات المستخدم

#### ✅ **Safari**
- **الأنظمة**: macOS فقط
- **المتطلبات**: يجب أن تكون مسجل الدخول في يودمي
- **الكشف**: كشف تلقائي لملفات تعريف ارتباط Safari (macOS فقط)

#### ✅ **Brave Browser**
- **الأنظمة**: Windows, macOS, Linux
- **المتطلبات**: يجب أن تكون مسجل الدخول في يودمي
- **الكشف**: كشف تلقائي لتثبيت Brave وبيانات المستخدم
- **ملاحظة**: يستخدم تنسيق ملفات تعريف الارتباط المشابه لـ Chrome

#### ✅ **Opera**
- **الأنظمة**: Windows, macOS, Linux
- **المتطلبات**: يجب أن تكون مسجل الدخول في يودمي
- **الكشف**: كشف تلقائي لتثبيت Opera وبيانات المستخدم

#### ✅ **Opera GX**
- **الأنظمة**: Windows, macOS, Linux
- **المتطلبات**: يجب أن تكون مسجل الدخول في يودمي
- **الكشف**: كشف تلقائي لتثبيت Opera GX وبيانات المستخدم
- **ملاحظة**: إصدار مخصص للألعاب من Opera

### كيف يعمل كشف المتصفح

1. **الكشف التلقائي**: التطبيق يبحث تلقائياً في نظامك عن المتصفحات المثبتة
2. **التحقق من ملفات تعريف الارتباط**: يفحص إذا كان كل متصفح يحتوي على ملفات تعريف ارتباط صالحة ليودمي
3. **واجهة ديناميكية**: يُظهر فقط المتصفحات المتاحة في نافذة تسجيل الدخول
4. **دعم احتياطي**: إذا لم يتم اكتشاف متصفحات، تسجيل الدخول بالبريد وكلمة المرور ما زال متاحاً

### عملية اختيار المتصفح

1. **متصفح واحد**: إذا كان متصفح واحد فقط متاح، يتم اختياره تلقائياً
2. **متصفحات متعددة**: إذا كانت متصفحات متعددة متاحة، يمكنك اختيار المفضل لديك
3. **لا توجد متصفحات**: إذا لم تكن متصفحات متاحة، يُظهر فقط تسجيل الدخول بالبريد وكلمة المرور

### استكشاف أخطاء المتصفح

#### "لا توجد متصفحات مدعومة"
- ثبت أحد المتصفحات المدعومة
- تأكد من أنك مسجل الدخول في يودمي في ذلك المتصفح
- استخدم تسجيل الدخول بالبريد وكلمة المرور كبديل

#### "فشل في تحميل ملفات تعريف الارتباط من [المتصفح]"
- تأكد من أنك مسجل الدخول في يودمي في المتصفح المختار
- أغلق وأعد تشغيل المتصفح
- امسح ذاكرة التخزين المؤقت للمتصفح وسجل الدخول مرة أخرى
- جرب متصفحاً آخر
- استخدم تسجيل الدخول بالبريد وكلمة المرور كبديل

#### "فشل في المصادقة"
- تحقق من أن جلسة يودمي الخاصة بك ما زالت نشطة
- سجل الخروج وسجل الدخول مرة أخرى في يودمي في متصفحك
- جرب استخدام تسجيل الدخول بالبريد وكلمة المرور بدلاً من ذلك

### أفضل الممارسات

1. **ابق مسجل الدخول**: اجعل جلسة يودمي نشطة في متصفحك المفضل
2. **استخدم المتصفح الأساسي**: استخدم المتصفح الذي تستخدمه عادة للتصفح
3. **احتفظ بملفات تعريف الارتباط**: لا تمسح ملفات تعريف الارتباط لـ udemy.com
4. **طريقة احتياطية**: تذكر دائماً أن تسجيل الدخول بالبريد وكلمة المرور متاح كنسخة احتياطية
