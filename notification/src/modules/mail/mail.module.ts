import { Module } from '@nestjs/common';
import { MailController } from './mail.controller';
import { MailService } from './mail.service';
import { TRANSPORTER } from './transporter';
import { ConfigModule } from '@nestjs/config';
import transporterConfig from '../../config/transporter.config';

@Module({
  imports: [ConfigModule.forRoot({ load: [transporterConfig] })],
  controllers: [MailController],
  providers: [MailService, TRANSPORTER],
})
export class MailModule {}
