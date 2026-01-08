# nginx

**Language:** he

nginx [נהגה: engine x] הוא שרת HTTP ופרוקסי הפוך, כמו גם שרת פרוקסי לדואר, שנכתב על ידי [Igor Sysoev](http://sysoev.ru/en/) . הוא נמצא בשימוש כבר יותר מחמש שנים באתרים רוסיים עמוסים במיוחד, כגון [Rambler](http://www.rambler.ru) (ו [RamblerMedia.com](http://ramblermedia.com) ). לפי חברת Netcraft, השרת nginx הגיש או נתן שירות ל [4.70% מהאתרים העמוסים ביותר באפריל 2010](http://news.netcraft.com/archives/2010/04/15/april_2010_web_server_survey.html) . הנה כמה סיפורי הצלחה: [FastMail.FM](http://blog.fastmail.fm/2007/01/04/webimappop-frontend-proxies-changed-to-nginx/) , [Wordpress.com](http://barry.wordpress.com/2008/04/28/load-balancer-update/) .

קוד המקור הוא בעל רשיון [2-פיסקאות דמוי רשיון BSD](/LICENSE) .

# תכונות HTTP בסיסיות {#basic_http_features}

- הגשת קבצים סטטיים וקובצי אינדקס, ואינדוקס אוטומטי;
מטמון file descriptor-ים פתוחים;
- פרוקסי הפוך מואץ כולל מטמון;
ביזור עומסים פשוט ושרידות מפני תקלות;
- תמיכה בהאצה עם מטמון של שרתי FastCGI מרוחקים;
ביזור עומסים פשוט ושרידות מפני תקלות;
- ארכיטקטורה מודולרית. פילטרים המבצעים gzip, טווחי בתים (byte ranges),
תשובות מסוג chunked, תמיכה ב XSLT, SSI ופילטר שינוי גודל תמונות.
ריבוי הכללות SSI בדף בודד יכול להיות מבוצע באופן מקבילי אם הן מטופלות
על ידי FastCGI או שרתים ש nginx הוא פרוקסי עבורם.
- תמיכה ב SSL ו TLS SNI.

# תכונות HTTP אחרות {#other_http_features}

- שרתים וירטואליים מבוססי IP ושם (הוסט);
- תמיכה ב keep-alive וב pipelining לחיבורים;
- תצורה גמישה;
- קביעת תצורה מחדש ואף שדרוג מקוון ללא כל הפרעה לעיבוד
בקשות הלקוחות;
- פורמטים ללוג הגישה, כתיבה ללוג באמצעות חוצץ, והחלפת לוגים מהירה;
- הפנייה באמצעות קודי שגיאה 3xx-5xx;
- מודול rewrite;
- בקרת גישה המבוססת על כתובת IP של הלקוח וגם אימות מסוג HTTP Basic;
- המתודות PUT, DELETE, MKCOL, COPY ו MOVE;
- סטרימינג של FLV;
- הגבלת מהירות;
- הגבלה של מספר החיבורים בו זמנית או מספר הבקשות מכתובת אחת.
- perl משובץ.

# תכונות פרוקסי דואר {#mail_proxy_server_features}

- הפניית משתמשים לשרתי IMAP/POP3 אחוריים בהתבסס על שרת אימות HTTP חיצוני;
- אימות משתמש באמצעות שרת אימות HTTP חיצוני והפניית חיבור לשרת SMTP פנימי;
- מתודות אימות:
  - POP3: USER/PASS, APOP, AUTH LOGIN/PLAIN/CRAM-MD5;
  - IMAP: LOGIN, AUTH LOGIN/PLAIN/CRAM-MD5;
  - SMTP: AUTH LOGIN/PLAIN/CRAM-MD5;
  
- תמיכה בהצפנת SSL;
- תמיכה ב STARTTLS ו STLS.

# ארכיטקטורה ויכולת גידול {#architecture_and_scalability}

- תהליך ראשי אחד ומספר תהליכי עובדים.
תהליכי העובדים רצים בתור משתמש ללא הרשאות;
- שיטות יידוע: kqueue (במערכות FreeBSD 4.1 ומעלה),
epoll (במערכות לינוקס 2.6 ומעלה), סיגנלי rt (במערכות לינוקס 2.2.19 ומעלה), `/dev/poll` (במערכות סולאריס 7 11/99 ומעלה), event ports (במערכות סולאריס 10),
select, ואף poll;
- תמיכה עבור תכונות kqueue שונות כולל  EV_CLEAR ו EV_DISABLE
(כדי לבטל אירועים זמנית), NOTE_LOWAT, EV_EOF, מספר קודי מידע ושגיאה;
- תמיכה ב sendfile (במערכות FreeBSD 3.1 ומעלה, לינוקס 2.2 ומעלה ו Mac OS X 10.5), תמיכה ב sendfile64 (לינוקס 2.4.21 ומעלה),
ו sendfilev (סולאריס 8 7/01 ומעלה);
- File AIO (במערכות FreeBSD 4.3 ומעלה ולינוקס 2.6.22 ומעלה);
- תמיכה ב Accept-filters (במערכות FreeBSD 4.1 ומעלה) ו TCP_DEFER_ACCEPT (במערכות לינוקס 2.4 ומעלה)
- 10,000 חיבורי HTTP לא פעילים במצב keep-alive תופסים נפח זיכרון העומד על בערך
12.5M;
- פעולות העתקת מידע מבוצעות באופן נדיר ככל האפשר.

# מערכות הפעלה ופלטפורמות בדוקות {#tested_os_and_platforms}

- FreeBSD 3—8 / i386; FreeBSD 5—8 / amd64;
- לינוקס 2.2—2.6 / i386; לינוקס 2.6 / amd64;
- סולאריס 9 / i386, sun4u; סולאריס 10 / i386, amd64, sun4v;
- MacOS X / ppc, i386;
- חלונות XP, חלונות סרבר 2003.

