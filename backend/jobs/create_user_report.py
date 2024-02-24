import sqlite3
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def create_pdf_of_users():
    def get_user_data():
        conn = sqlite3.connect('./database/database.db')  
        cursor = conn.cursor()

        cursor.execute('''
            SELECT u.id, u.name, u.email, 
                COUNT(ub.book_id) AS books_issued,
                GROUP_CONCAT(DISTINCT s.name) AS sections_issued_from,
                GROUP_CONCAT(DISTINCT ub.date_of_issue) AS dates_of_issue,
                GROUP_CONCAT(DISTINCT b.name) AS book_names,
                GROUP_CONCAT(DISTINCT ub.date_of_issue) AS issue_dates,
                GROUP_CONCAT(DISTINCT ub.return_date) AS return_dates,
                GROUP_CONCAT(DISTINCT ub.returned) AS returned_statuses
            FROM users u
            LEFT JOIN user_books ub ON u.id = ub.user_id
            LEFT JOIN books b ON ub.book_id = b.id
            LEFT JOIN books_allocation ba ON ub.book_id = ba.book_id
            LEFT JOIN sections s ON ba.section_id = s.id
            GROUP BY u.id
        ''')
        user_data = cursor.fetchall()

        conn.close()

        user_details = {}
        for user_info in user_data:
            user_id = user_info[0]
            sections_issued_from = user_info[4].split(',') if user_info[4] is not None else []
            dates_of_issue = user_info[5].split(',') if user_info[5] is not None else []
            book_names = user_info[6].split(',') if user_info[6] is not None else []
            issue_dates = user_info[7].split(',') if user_info[7] is not None else []
            return_dates = user_info[8].split(',') if user_info[8] is not None else []
            returned_statuses = user_info[9].split(',') if user_info[9] is not None else []
            
            # Zip book details with return status
            user_books_info = []
            for book_name, issued_on, returned_on, returned_status in zip(book_names, issue_dates, return_dates, returned_statuses):
                book_info = {
                    'book_name': book_name,
                    'issued_on': issued_on,
                    'returned_on': returned_on,
                    'returned': returned_status == '1'
                }
                user_books_info.append(book_info)
            
            user_details[user_id] = {
                'name': user_info[1],
                'email': user_info[2],
                'books_issued': user_info[3],
                'sections_issued_from': sections_issued_from,
                'user_books_info': user_books_info
            }

        return user_details

    def generate_user_pdf(user_id, user_details, folder_path):
        details = user_details[user_id]
        pdf_filename = f"{user_id}.pdf"  
        pdf_path = os.path.join(folder_path, pdf_filename)
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        heading = Paragraph(f"<b>Here is the Summary of your Activity, {details['name'] }</b>", styles['Title'])
        elements.append(heading)
        elements.append(Table([['']]))  

        user_details_table = Table([
            ['User ID:', user_id],
            ['Name:', details['name']],
            ['Email:', details['email']],
            ['Books Issued:', details['books_issued']],
            ['Sections Issued From:', ', '.join(details['sections_issued_from'])],
        ])
        user_details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        elements.append(user_details_table)
        elements.append(Table([['']]))  

        book_details_heading_style = ParagraphStyle(name="CenteredHeading", alignment=1, parent=styles["Heading2"])
        book_details_heading = Paragraph("<b>Book Details</b>", book_details_heading_style)
        elements.append(book_details_heading)
        elements.append(Table([['']]))  

        book_info_data = [['Book Name', 'Issued On', 'Returned On', 'Returned']]
        for book_info in details['user_books_info']:
            returned_on = book_info['returned_on'] if book_info['returned'] else 'Not Returned'
            book_info_data.append([book_info['book_name'], book_info['issued_on'], returned_on, 'Yes' if book_info['returned'] else 'No'])
        book_info_table = Table(book_info_data)
        book_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ]))
        elements.append(book_info_table)

        doc.build(elements)

    folder_path = "user_pdfs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    user_data = get_user_data()
    for user_id in user_data.keys():
        generate_user_pdf(user_id, user_data, folder_path)

    print("PDFs created successfully.")


create_pdf_of_users()