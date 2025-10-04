import { Body, Controller, Post } from '@nestjs/common';
import { SendMailDto } from '../../dto/send_mail.dto';

@Controller('mail')
export class DevMailController {
  @Post()
  async sendMail(@Body() data: SendMailDto) {
    console.log('Send mail:');
    Object.keys(data).forEach((key) => console.log(key, data[key]));
    return;
  }
}
