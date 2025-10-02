import { Body, Controller, Post } from '@nestjs/common';
import { SendMailDto } from './dto/send_mail.dto';
import { MailService } from './mail.service';

@Controller('mail')
export class MailController {
  constructor(private readonly mailService: MailService) {}
  @Post()
  async sendMail(@Body() data: SendMailDto) {
    return await this.mailService.sendMail(data);
  }
}
