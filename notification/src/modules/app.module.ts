import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import appConfig from '../config/app.config';
import { MailModule } from './mail/mail.module';

@Module({
  imports: [ConfigModule.forRoot({ load: [appConfig] }), MailModule],
  controllers: [],
  providers: [],
})
export class AppModule {}
