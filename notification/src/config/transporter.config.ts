import { registerAs } from '@nestjs/config';
import * as process from 'node:process';

export default registerAs('transporter', () => ({
  host: String(process.env.SMTP_HOST),
  port: Number(process.env.SMTP_PORT),
  user: Number(process.env.SMTP_USER),
  pass: Number(process.env.SMTP_PASS),
}));
