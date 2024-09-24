import json
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class MailSendView(TemplateView):

    def post(self, request, *args, **kwargs):
        print(self.__dict__)
        send_to = request.POST.get('send_to')
        subject = request.POST.get('subject')

        if not (subject and send_to):
            return HttpResponse(
                json.dumps({'result': {'status': 'error', 'message': 'Missing send_to'}}),
                content_type='application/json',
                status=400
            )

        # Define email roles and templates
        email_data = [
            # Customer Emails
            # 'customer/package_booking.html',
            'customer/package_booking_cancellation.html',
            # 'customer/package_refund.html',
            # 'customer/package_enquiry.html',

            # Agent Emails
            # 'agent/package_enquiry.html',
            # 'agent/package_booking.html',
            # 'agent/package_approval.html',
            # 'agent/package_payment_transaction.html',
            # 'agent/package_booking_cancellation.html',
            
            # Admin Emails
            # 'admin/package_enquiry.html',
            # 'admin/package_booking.html',
            # 'admin/package_booking_status_change.html',
            # 'admin/package_booking_submission.html',
            # 'admin/package_booking_cancellation.html',
        ]
        
        # Loop through the email data and send each email
        for template in email_data:
            user = template.split('/')[0].capitalize()
            template_name = template.split('/')[1].replace('.html', '').replace('_', ' ').title()
            # Create dynamic subject
            email_subject = f"{subject} | {user} | {template_name}"
            
            email_body = render_to_string(template, {'name': 'Thamjid'})

            # Create the email message
            mail = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=send_to.split(','),
            )
            mail.content_subtype = 'html'
            mail.mixed_subtype = 'related'

            # Try to send the email
            try:
                mail.send()
            except Exception as error:
                print(str(error))
                return HttpResponse(
                    json.dumps({'result': {'status': 'error', 'message': str(error)}}),
                    content_type='application/json',
                    status=500
                )

        # Return success response after all emails are sent
        return HttpResponse(
            json.dumps({'result': {'status': 'success'}}),
            content_type='application/json',
            status=200
        )
