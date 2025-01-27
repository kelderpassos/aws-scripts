import { DynamoManager } from './dynamodb/DynamoManager';
import {
  EXPORT_ITEMS_QUEUE,
  PROVISION_TABLES_QUEUE,
  WRITE_ITEMS_QUEUE,
  REGION,
  roleToAssume
  // mockedTableNames // use for tests
} from './helpers/constants';
import { SqsManager } from './sqs/SqsHandler';
import { StsManager } from './sts/StsManager';

export const handler = async (): Promise<void> => {
  console.log('Backup routine invoked');

  const sts = new StsManager(REGION, roleToAssume);
  const credentials = await sts.assumeRole();

  const originalDynamo = new DynamoManager(REGION, credentials);

  const exportItemsToS3Queue = new SqsManager(EXPORT_ITEMS_QUEUE, REGION);
  const provisionTableQueue = new SqsManager(PROVISION_TABLES_QUEUE, REGION);
  const writeItemsQueue = new SqsManager(WRITE_ITEMS_QUEUE, REGION);

  const tableNames = await originalDynamo.listTables();
  console.log('TABLENAMES', tableNames);

  for (const table of tableNames) {
    try {
      // await originalDynamo.populateTable(table); to populate the mock tables with some data

      await exportItemsToS3Queue.sendMessage(table);
      await provisionTableQueue.sendMessage(table);
      await writeItemsQueue.sendMessage(table);
    } catch (error) {
      console.log('Error backup routine lambda', error);
      throw error;
    }
  }
};
