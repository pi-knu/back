import { Inject, Injectable } from '@nestjs/common';
import * as nodemailer from 'nodemailer';
import { TRANSPORTER_TOKEN } from './transporter';
import { SendMailDto } from './dto/send_mail.dto';

@Injectable()
export class MailService {
  constructor(
    @Inject(TRANSPORTER_TOKEN)
    private readonly transporter: nodemailer.Transporter,
  ) {}

  async sendMail(data: SendMailDto) {
    return this.transporter.sendMail({
      from: `"My App" <${process.env.SMTP_USER}>`,
      ...data,
    });
  }
}
