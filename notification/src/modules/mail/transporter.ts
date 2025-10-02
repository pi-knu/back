import * as nodemailer from 'nodemailer';
import { ConfigType } from '@nestjs/config';
import transporterConfig from '../../config/transporter.config';
import { Provider } from '@nestjs/common';

export const TRANSPORTER_TOKEN = 'MAIL_TRANSPORTER';

export const TRANSPORTER: Provider = {
  provide: TRANSPORTER_TOKEN,
  inject: [transporterConfig.KEY],
  useFactory: (transporterConf: ConfigType<typeof transporterConfig>) => {
    return nodemailer.createTransport({
      host: transporterConf.host,
      port: transporterConf.port,
      secure: false,
      auth: {
        user: transporterConf.user,
        pass: transporterConf.pass,
      },
    } as nodemailer.TransportOptions);
  },
};
