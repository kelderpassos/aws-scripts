import { randomBytes } from 'crypto';

export const EXPORT_ITEMS_QUEUE = process.env
  .EXPORT_ITEMS_TO_S3_FIFO_QUEUE as string;
export const PROVISION_TABLES_QUEUE = process.env.PROVISION_TABLES_QUEUE as string;
export const WRITE_ITEMS_QUEUE = process.env.WRITE_ITEMS_QUEUE as string;

export const ROLE_TO_ASSUME = process.env.ROLE_TO_ASSUME as string;
export const ORIGIN_ACCOUNT_ID = process.env.ORIGIN_ACCOUNT_ID as string;
export const BACKUP_ACCOUNT_ID = process.env.BACKUP_ACCOUNT_ID as string;
export const BUCKET_NAME = process.env.BUCKET_NAME as string;
export const REGION = process.env.REGION as string;
export const SLACK_WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL as string;

export const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

const day = new Date().getDate();
const month = new Date().getMonth() + 1;
const year = new Date().getFullYear();

export const timestamp = {
  day: day < 10 ? `0${day}` : day,
  month: month < 10 ? `0${month}` : month,
  year,
};

export const generateObjectKey = (tableName: string): string =>
  `backup-${tableName}-${day}-${month}-${year}`;

const DURATION_SECONDS = 900; // 15 minutes, same time as the lambda timeout

export const roleToAssume = {
  RoleArn: `arn:aws:iam::${ORIGIN_ACCOUNT_ID}:role/${ROLE_TO_ASSUME}`,
  RoleSessionName: 'session1',
  DurationSeconds: DURATION_SECONDS,
};

export const mockedTableNames = [
  'tabela-teste-01',
  'tabela-teste-02',
  'tabela-teste-03',
  'tabela-teste-04',
  'tabela-teste-05',
  'tabela-teste-06',
  'tabela-teste-07',
  'tabela-teste-08',
  'tabela-teste-09',
  'tabela-teste-10',
  'tabela-teste-11',
  'tabela-teste-12',
];

export const data = {
  M: {
    name: { S: `Nome-${randomBytes(10)}` },
    age: { N: randomBytes(10).toString() },
    role: { S: `Role-${randomBytes(10)}` },
    class: { S: `Class-${randomBytes(10)}` },
    origin: { S: `Origin-${randomBytes(10)}` },
    destiny: { S: `Destiny-${randomBytes(10)}` },
    description: { S: `Description-${randomBytes(10)}` },
    email: { S: `Email-${randomBytes(10)}` },
    phone: { S: `Phone-${randomBytes(10)}` },
    address: { S: `Address-${randomBytes(10)}` },
    city: { S: `City-${randomBytes(10)}` },
    state: { S: `State-${randomBytes(10)}` },
    country: { S: `Country-${randomBytes(10)}` },
    postalCode: { S: `PostalCode-${randomBytes(10)}` },
    checker1: { S: `Checker-${randomBytes(10)}` },
    checker2: { S: `Checker2-${randomBytes(10)}` },
    checker3: { S: `Checker3-${randomBytes(10)}` },
    checker4: { S: `Checker4-${randomBytes(10)}` },
    checker5: { S: `Checker5-${randomBytes(10)}` },
    checker6: { S: `Checker6-${randomBytes(10)}` },
    checker7: { S: `Checker7-${randomBytes(10)}` },
    checker8: { S: `Checker8-${randomBytes(10)}` },
    checker9: { S: `Checker9-${randomBytes(10)}` },
    checker10: { S: `Checker10-${randomBytes(10)}` },
    checker11: { S: `Checker11-${randomBytes(10)}` },
    checker12: { S: `Checker12-${randomBytes(10)}` },
    checker13: { S: `Checker13-${randomBytes(10)}` },
    checker14: { S: `Checker14-${randomBytes(10)}` },
    checker15: { S: `Checker15-${randomBytes(10)}` },
    checker16: { S: `Checker16-${randomBytes(10)}` },
    checker17: { S: `Checker17-${randomBytes(10)}` },
    checker18: { S: `Checker18-${randomBytes(10)}` },
    checker19: { S: `Checker19-${randomBytes(10)}` },
    checker20: { S: `Checker20-${randomBytes(10)}` },
    checker21: { S: `Checker21-${randomBytes(10)}` },
    checker22: { S: `Checker22-${randomBytes(10)}` },
    checker23: { S: `Checker23-${randomBytes(10)}` },
    checker24: { S: `Checker24-${randomBytes(10)}` },
    checker25: { S: `Checker25-${randomBytes(10)}` },
    checker26: { S: `Checker26-${randomBytes(10)}` },
    checker27: { S: `Checker27-${randomBytes(10)}` },
    checker28: { S: `Checker28-${randomBytes(10)}` },
    checker29: { S: `Checker29-${randomBytes(10)}` },
    checker30: { S: `Checker30-${randomBytes(10)}` },
    checker31: { S: `Checker31-${randomBytes(10)}` },
    checker32: { S: `Checker32-${randomBytes(10)}` },
    checker33: { S: `Checker33-${randomBytes(10)}` },
    checker34: { S: `Checker34-${randomBytes(10)}` },
    checker35: { S: `Checker35-${randomBytes(10)}` },
  },
};
