import { Module } from '@nestjs/common';
import { MailController } from './mail.controller';
import { MailService } from './mail.service';
import { TRANSPORTER } from './transporter';

@Module({
  imports: [],
  controllers: [MailController],
  providers: [MailService, TRANSPORTER],
})
export class MailModule {}
