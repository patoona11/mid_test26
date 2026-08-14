import psycopg2
import os

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:midtest%402026@db.somnbanbnkhzfqyhmxnb.supabase.co:5432/postgres")

def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

def seed():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print("Dropping existing tables if any...")
    cursor.execute('DROP TABLE IF EXISTS scores')
    cursor.execute('DROP TABLE IF EXISTS questions')
    cursor.execute('DROP TABLE IF EXISTS categories')
    cursor.execute('DROP TABLE IF EXISTS students')

    print("Creating tables...")
    cursor.execute('''
        CREATE TABLE categories (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE students (
            id SERIAL PRIMARY KEY,
            student_code INTEGER NOT NULL UNIQUE,
            fullname TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE questions (
            id SERIAL PRIMARY KEY,
            category_id INTEGER,
            question_text TEXT NOT NULL,
            choice_a TEXT NOT NULL,
            choice_b TEXT NOT NULL,
            choice_c TEXT NOT NULL,
            choice_d TEXT NOT NULL,
            choice_e TEXT,
            correct_answer TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE scores (
            id SERIAL PRIMARY KEY,
            student_id INTEGER,
            score INTEGER NOT NULL,
            total_score INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')

    print("Seeding data...")
    # Seed Categories
    categories = [
        ('บทที่ 1: ความรู้เบื้องต้นเกี่ยวกับคอมพิวเตอร์และอุปกรณ์',),
        ('บทที่ 2: ระบบเครือข่ายคอมพิวเตอร์เบื้องต้น',),
        ('บทที่ 3: ระบบปฏิบัติการ (Operating System)',),
        ('บทที่ 4: การใช้งานโปรแกรมประยุกต์เบื้องต้น',),
        ('บทที่ 5: ความปลอดภัยและจริยธรรมในการใช้คอมพิวเตอร์',)
    ]
    cursor.executemany('INSERT INTO categories (name) VALUES (%s)', categories)

    # Seed Questions (10 per category)
    # Category 1
    questions_c1 = [
        (1, 'ข้อใดคือความหมายของคอมพิวเตอร์', 'อุปกรณ์ที่สามารถคำนวณได้', 'อุปกรณ์อิเล็กทรอนิกส์ที่สามารถทำงานได้ด้วยคำสั่งของมนุษย์', 'โปรแกรมสำหรับเล่นเกมได้', 'ระบบงานโปรแกรมที่สามารถถ่ายโอนข้อมูลได้', 'อุปกรณ์ที่ใช้ไฟฟ้าในการควบคุมการทำงาน', 'ข'),
        (1, 'จอภาพเป็นอุปกรณ์ประเภทใด', 'รับข้อมูล', 'ประมวลผลข้อมูล', 'แสดงผลข้อมูล', 'จัดเก็บข้อมูล', 'ควบคุมข้อมูล', 'ค'),
        (1, 'หน่วยประมวลผลกลางของคอมพิวเตอร์เรียกว่าอะไร', 'RAM', 'ROM', 'CPU', 'Hard Disk', 'Motherboard', 'ค'),
        (1, 'อุปกรณ์ใดต่อไปนี้ทำหน้าที่รับข้อมูลเข้าสู่คอมพิวเตอร์', 'จอภาพ', 'ลำโพง', 'เมาส์', 'เครื่องพิมพ์', 'เครื่องฉายโปรเจคเตอร์', 'ค'),
        (1, 'RAM มีหน้าที่หลักอย่างไร', 'เก็บข้อมูลถาวร', 'เก็บข้อมูลชั่วคราวขณะเครื่องทำงาน', 'ประมวลผลคำสั่ง', 'พิมพ์งานเอกสาร', 'เชื่อมต่อเครือข่าย', 'ข'),
        (1, 'ความแตกต่างระหว่าง Hardware และ Software คืออะไร', 'Hardware สัมผัสได้ Software สัมผัสไม่ได้', 'Software สัมผัสได้ Hardware สัมผัสไม่ได้', 'ไม่มีความแตกต่าง', 'เป็นชื่อเรียกของอุปกรณ์อิเล็กทรอนิกส์เหมือนกัน', 'Hardware ทำงานเร็วกว่า Software', 'ก'),
        (1, 'หน่วยเก็บข้อมูลใดมีความเร็วในการเข้าถึงข้อมูลมากที่สุด', 'Hard Disk', 'USB Flash Drive', 'RAM', 'CD-ROM', 'SSD', 'ค'),
        (1, 'ข้อใดไม่ใช่ส่วนประกอบของคอมพิวเตอร์', 'หน่วยรับข้อมูล', 'หน่วยประมวลผลกลาง', 'หน่วยความจำ', 'หน่วยพลังงาน', 'หน่วยแสดงผล', 'ง'),
        (1, 'อุปกรณ์ใดใช้สำหรับเก็บข้อมูลระยะยาวและมีขนาดความจุสูง', 'RAM', 'Cache', 'ROM', 'Hard Disk Drive', 'Keyboard', 'ง'),
        (1, 'การเปิดเครื่องคอมพิวเตอร์เรียกว่าอะไร', 'Restart', 'Boot', 'Shutdown', 'Sleep', 'Log off', 'ข')
    ]

    # Category 2
    questions_c2 = [
        (2, 'LAN ย่อมาจากคำว่าอะไร', 'Local Area Network', 'Large Area Network', 'Local Access Network', 'Long Area Network', 'Low Access Network', 'ก'),
        (2, 'เครือข่ายคอมพิวเตอร์หมายถึงอะไร', 'การนำคอมพิวเตอร์ 2 เครื่องขึ้นไปมาเชื่อมต่อกัน', 'การใช้คอมพิวเตอร์เครื่องเดียวพิมพ์งาน', 'การเล่นเกมบนคอมพิวเตอร์', 'การเขียนโปรแกรมคอมพิวเตอร์', 'การซ่อมแซมคอมพิวเตอร์', 'ก'),
        (2, 'ข้อใดคือลักษณะของเครือข่าย WAN', 'เชื่อมต่อภายในห้องเดียวกัน', 'เชื่อมต่อภายในอาคารเดียวกัน', 'เชื่อมต่อระหว่างประเทศหรือภูมิภาค', 'เชื่อมต่อเฉพาะโทรศัพท์มือถือ', 'ไม่มีข้อใดถูก', 'ค'),
        (2, 'IP Address คืออะไร', 'หมายเลขโทรศัพท์', 'หมายเลขประจำเครื่องคอมพิวเตอร์ในเครือข่าย', 'รหัสผ่านของระบบ', 'ชื่อผู้ใช้', 'ที่อยู่ของเว็บไซต์', 'ข'),
        (2, 'อุปกรณ์ใดทำหน้าที่เชื่อมต่อเครือข่ายที่ต่างกันเข้าด้วยกัน', 'Hub', 'Switch', 'Router', 'Repeater', 'Modem', 'ค'),
        (2, 'โปรโตคอล (Protocol) คืออะไร', 'ภาษาคอมพิวเตอร์', 'กฎระเบียบและข้อตกลงในการสื่อสารข้อมูล', 'โปรแกรมป้องกันไวรัส', 'อุปกรณ์กระจายสัญญาณ', 'สายสัญญาณเครือข่าย', 'ข'),
        (2, 'ข้อใดคือตัวอย่างของโปรโตคอลที่ใช้ในการโอนย้ายไฟล์', 'HTTP', 'FTP', 'SMTP', 'POP3', 'DHCP', 'ข'),
        (2, 'Wi-Fi คือการเชื่อมต่อเครือข่ายแบบใด', 'แบบมีสาย', 'แบบไร้สาย', 'แบบผสม', 'แบบดาวเทียม', 'แบบใยแก้วนำแสง', 'ข'),
        (2, 'URL คืออะไร', 'ที่อยู่ของเว็บไซต์', 'รหัสผ่าน', 'ชื่อผู้ใช้', 'หมายเลขเครื่อง', 'ประเภทไฟล์', 'ก'),
        (2, 'ข้อใดคือหน้าที่ของ DNS (Domain Name System)', 'แปลงชื่อโดเมนเป็น IP Address', 'แปลง IP Address เป็นชื่อโดเมน', 'ป้องกันไวรัส', 'กระจายสัญญาณเครือข่าย', 'ถูกทั้ง ก และ ข', 'จ')
    ]

    # Category 3
    questions_c3 = [
        (3, 'ข้อใดคือระบบปฏิบัติการสำหรับคอมพิวเตอร์ส่วนบุคคลที่นิยมใช้มากที่สุด', 'Linux', 'macOS', 'Windows', 'Android', 'iOS', 'ค'),
        (3, 'ระบบปฏิบัติการใดที่เป็นระบบปฏิบัติการแบบ Open Source', 'Windows', 'macOS', 'Linux', 'iOS', 'MS-DOS', 'ค'),
        (3, 'หน้าที่หลักของระบบปฏิบัติการคืออะไร', 'สร้างเอกสาร', 'จัดการทรัพยากรของระบบคอมพิวเตอร์', 'ป้องกันไวรัส', 'เล่นเกม', 'ท่องอินเทอร์เน็ต', 'ข'),
        (3, 'ข้อใดคือตัวอย่างของระบบปฏิบัติการบนสมาร์ทโฟน', 'Windows 10', 'macOS', 'Android', 'Linux', 'Unix', 'ค'),
        (3, 'GUI ย่อมาจากอะไร', 'General User Interface', 'Graphical User Interface', 'Global User Interface', 'Graphic Utility Interface', 'General Utility Interface', 'ข'),
        (3, 'ข้อใดไม่ใช่ระบบปฏิบัติการ', 'Windows', 'Linux', 'macOS', 'Microsoft Office', 'Android', 'ง'),
        (3, 'การทำ Multitasking คืออะไร', 'การทำงานได้หลายอย่างพร้อมกัน', 'การทำงานได้เพียงอย่างเดียว', 'การปิดเครื่องอัตโนมัติ', 'การสำรองข้อมูล', 'การทำความสะอาดระบบ', 'ก'),
        (3, 'File System (ระบบไฟล์) ทำหน้าที่อะไร', 'จัดการการจัดเก็บข้อมูลบนสื่อบันทึกข้อมูล', 'ป้องกันไวรัส', 'เชื่อมต่ออินเทอร์เน็ต', 'แสดงผลภาพ', 'พิมพ์เอกสาร', 'ก'),
        (3, 'ข้อใดคือคำสั่งที่ใช้ในการแสดงรายชื่อไฟล์ในระบบ DOS หรือ Command Prompt', 'dir', 'ls', 'cd', 'copy', 'del', 'ก'),
        (3, 'ระบบปฏิบัติการ Unix เป็นระบบปฏิบัติการประเภทใด', 'Single-user, Single-tasking', 'Single-user, Multi-tasking', 'Multi-user, Multi-tasking', 'Open Source เสมอ', 'ไม่มีข้อใดถูก', 'ค')
    ]

    # Category 4
    questions_c4 = [
        (4, 'โปรแกรมใดเหมาะสำหรับการพิมพ์รายงานมากที่สุด', 'Microsoft Excel', 'Microsoft PowerPoint', 'Microsoft Word', 'Microsoft Access', 'Microsoft Publisher', 'ค'),
        (4, 'หากต้องการสร้างตารางคำนวณ ควรใช้โปรแกรมใด', 'Microsoft Word', 'Microsoft Excel', 'Microsoft PowerPoint', 'Microsoft Access', 'Notepad', 'ข'),
        (4, 'ข้อใดคือนามสกุลไฟล์ของ Microsoft Word 2007 ขึ้นไป', '.doc', '.docx', '.txt', '.pdf', '.xls', 'ข'),
        (4, 'โปรแกรมที่ใช้ในการนำเสนองาน (Presentation) คือโปรแกรมใด', 'Microsoft Word', 'Microsoft Excel', 'Microsoft PowerPoint', 'Microsoft Access', 'Paint', 'ค'),
        (4, 'ฟังก์ชัน SUM ใน Excel ใช้ทำอะไร', 'หาค่าเฉลี่ย', 'หาผลรวม', 'นับจำนวน', 'หาค่าสูงสุด', 'หาค่าต่ำสุด', 'ข'),
        (4, 'หากต้องการคัดลอกข้อความ (Copy) ต้องใช้คีย์ลัดใด', 'Ctrl + C', 'Ctrl + V', 'Ctrl + X', 'Ctrl + Z', 'Ctrl + P', 'ก'),
        (4, 'คีย์ลัดใดใช้สำหรับการวางข้อความ (Paste)', 'Ctrl + C', 'Ctrl + V', 'Ctrl + X', 'Ctrl + Z', 'Ctrl + P', 'ข'),
        (4, 'โปรแกรม Web Browser ใช้ทำหน้าที่อะไร', 'ดูหนัง', 'ฟังเพลง', 'เข้าชมเว็บไซต์', 'พิมพ์งาน', 'คำนวณตัวเลข', 'ค'),
        (4, 'ข้อใดต่อไปนี้ไม่ใช่ Web Browser', 'Google Chrome', 'Mozilla Firefox', 'Microsoft Edge', 'Microsoft Word', 'Safari', 'ง'),
        (4, 'การเซฟไฟล์งาน (Save) เพื่อบันทึกการเปลี่ยนแปลงใช้คีย์ลัดใด', 'Ctrl + S', 'Ctrl + P', 'Ctrl + O', 'Ctrl + N', 'Ctrl + W', 'ก')
    ]

    # Category 5
    questions_c5 = [
        (5, 'ข้อใดคือพฤติกรรมที่ไม่เหมาะสมในการใช้อินเทอร์เน็ต', 'ใช้อินเทอร์เน็ตหาข้อมูลทำรายงาน', 'โพสต์ข้อความด่าทอผู้อื่น', 'ส่งอีเมลหางาน', 'ซื้อของออนไลน์อย่างระมัดระวัง', 'อ่านข่าวสาร', 'ข'),
        (5, 'พาสเวิร์ด (Password) ที่ดีควรมีลักษณะอย่างไร', 'ตั้งให้เดาง่ายๆ เช่น 1234', 'ใช้วันเกิดของตนเอง', 'ใช้ตัวอักษรผสมตัวเลขและสัญลักษณ์', 'ใช้ชื่อเล่นของตนเอง', 'จดไว้ในกระดาษแปะหน้าจอคอม', 'ค'),
        (5, 'ไวรัสคอมพิวเตอร์คืออะไร', 'สิ่งมีชีวิตที่ทำให้คอมพิวเตอร์พัง', 'โปรแกรมที่เขียนขึ้นเพื่อประสงค์ร้าย', 'ฝุ่นที่เกาะอยู่ในคอมพิวเตอร์', 'ความร้อนของเครื่องคอมพิวเตอร์', 'ข้อผิดพลาดของระบบปฏิบัติการ', 'ข'),
        (5, 'การนำผลงานของผู้อื่นมาแอบอ้างว่าเป็นของตนเองเรียกว่าอะไร', 'การโจรกรรม', 'การทำสำเนา', 'การลอกเลียนวรรณกรรม (Plagiarism)', 'การอ้างอิง', 'การแชร์ข้อมูล', 'ค'),
        (5, 'ข้อใดคือวิธีป้องกันไวรัสคอมพิวเตอร์ที่ดีที่สุด', 'ไม่เปิดคอมพิวเตอร์', 'ติดตั้งโปรแกรมแอนตี้ไวรัสและอัปเดตสม่ำเสมอ', 'ล้างข้อมูลในฮาร์ดดิสก์ทุกวัน', 'ไม่เชื่อมต่ออินเทอร์เน็ตเลย', 'เปลี่ยนคอมพิวเตอร์ใหม่ทุกปี', 'ข'),
        (5, 'Phishing คืออะไร', 'การตกปลา', 'การหลอกลวงทางอินเทอร์เน็ตเพื่อขโมยข้อมูลส่วนตัว', 'การเขียนโปรแกรม', 'การซ่อมคอมพิวเตอร์', 'การส่งอีเมลขยะ', 'ข'),
        (5, 'หากได้รับอีเมลแนบไฟล์จากคนที่ไม่รู้จัก ควรทำอย่างไร', 'รีบเปิดดูทันที', 'ลบทิ้งหรือส่งไปที่ Junk Mail', 'ส่งต่อให้เพื่อน', 'ตอบกลับอีเมล', 'โหลดมาเก็บไว้ในเครื่อง', 'ข'),
        (5, 'ลิขสิทธิ์ (Copyright) หมายถึงอะไร', 'สิทธิผูกขาดของผู้สร้างสรรค์ผลงาน', 'การอนุญาตให้คัดลอกผลงานได้เสรี', 'เครื่องหมายการค้า', 'สิทธิบัตรการประดิษฐ์', 'ความลับทางการค้า', 'ก'),
        (5, 'การกระทำใดถือเป็นการละเมิดลิขสิทธิ์ซอฟต์แวร์', 'ซื้อซอฟต์แวร์ของแท้มาใช้งาน', 'ดาวน์โหลดซอฟต์แวร์เถื่อนมาใช้งาน', 'ใช้ซอฟต์แวร์แบบ Open Source', 'ใช้ซอฟต์แวร์แบบ Freeware', 'อัปเดตซอฟต์แวร์แท้', 'ข'),
        (5, 'พรบ. คอมพิวเตอร์ มีไว้เพื่ออะไร', 'เพื่อให้คนใช้คอมพิวเตอร์เก่งขึ้น', 'ควบคุมการผลิตคอมพิวเตอร์', 'ป้องกันและปราบปรามการกระทำความผิดเกี่ยวกับคอมพิวเตอร์', 'สนับสนุนการเล่นเกมออนไลน์', 'ลดราคาอุปกรณ์คอมพิวเตอร์', 'ค')
    ]

    all_questions = questions_c1 + questions_c2 + questions_c3 + questions_c4 + questions_c5
    
    cursor.executemany('''
        INSERT INTO questions (category_id, question_text, choice_a, choice_b, choice_c, choice_d, choice_e, correct_answer) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', all_questions)

    conn.commit()
    conn.close()
    print("Supabase PostgreSQL Database successfully seeded!")

if __name__ == '__main__':
    seed()
