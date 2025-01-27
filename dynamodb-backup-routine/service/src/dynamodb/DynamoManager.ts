import {
  DynamoDB,
  ListTablesCommand,
  CreateTableCommand,
  DescribeTableCommand,
  CreateTableCommandInput,
  PutItemCommandInput,
  PutItemCommand,
  AttributeValue,
  ScanCommand,
} from '@aws-sdk/client-dynamodb';
import { ExportedItems, TableConfig, TableItems } from '../helpers/interfaces';
import { data } from '../helpers/constants';

export class DynamoManager {
  private readonly client: DynamoDB;

  constructor(
    private region: string,
    private credentials: any,
  ) {
    this.client = new DynamoDB({
      region: this.region,
      credentials: this.credentials,
    });
  }

  private createTables = async (config: CreateTableCommandInput) => {
    try {
      const createTableCommand = new CreateTableCommand(config);
      await this.client.send(createTableCommand);
    } catch (error) {
      console.log(`Error creating table ${config.TableName}`, error);
      throw error;
    }
  };

  public readonly listTables = async () => {
    const command = new ListTablesCommand({});
    const tables = await this.client.send(command);
    if (!tables.TableNames) return [];

    const actualTables = tables.TableNames.filter(
      (name) => !name.includes('AmplifyDataStore'),
    );

    return actualTables;
  };

  public exportItems = async (
    table: string,
    lastEvaluatedKey: Record<string, AttributeValue> | undefined,
  ): Promise<ExportedItems> => {
    try {
      const command = new ScanCommand({
        TableName: table,
        ExclusiveStartKey: lastEvaluatedKey,
      });

      const { Items, LastEvaluatedKey } = await this.client.send(command);
      if (LastEvaluatedKey) {
        const nextItems = await this.exportItems(table, LastEvaluatedKey);
        return { Items: (Items ?? []).concat(nextItems.Items) };
      }

      return { Items: Items ?? [] };
    } catch (error) {
      console.log('Error exporting items', error);
      throw error;
    }
  };

  public describeTable = async (tableName: string): Promise<TableConfig> => {
    const command = new DescribeTableCommand({ TableName: tableName });
    const tableDescription = await this.client.send(command);
    const globalSecondaryIndexesMap =
      tableDescription.Table?.GlobalSecondaryIndexes?.map((index) => ({
        IndexName: index.IndexName,
        KeySchema: index.KeySchema,
        Projection: index.Projection,
      }));

    const newTableConfig: TableConfig = {
      TableName: tableDescription.Table?.TableName ?? tableName,
      KeySchema: tableDescription.Table?.KeySchema,
      GlobalSecondaryIndexes: globalSecondaryIndexesMap,
      AttributeDefinitions: tableDescription.Table?.AttributeDefinitions,
      BillingMode: tableDescription.Table?.BillingModeSummary?.BillingMode,
      ProvinedThroughput:
        tableDescription.Table?.BillingModeSummary?.BillingMode ===
        'PAY_PER_REQUEST'
          ? undefined
          : {
              ReadCapacityUnits:
                tableDescription.Table?.ProvisionedThroughput
                  ?.ReadCapacityUnits,
              WriteCapacityUnits:
                tableDescription.Table?.ProvisionedThroughput
                  ?.WriteCapacityUnits,
            },
    };

    return newTableConfig;
  };

  public provisionTables = async (description: TableConfig) => {
    const existingTable = await this.listTables();
    if (existingTable.includes(description.TableName)) {
      console.log(
        `Table ${description.TableName} already exists, skipping createTable`,
      );
      return;
    }

    await this.createTables(description);
    console.log(`Table ${description.TableName} provisioned`);
  };

  public writeBackup = async (tableName: string, items: TableItems) => {
    for (const item of items) {
      const params: PutItemCommandInput = {
        TableName: tableName,
        Item: item,
      };
      try {
        const command = new PutItemCommand(params);
        await this.client.send(command);
      } catch (error) {
        console.log(`Error writing backup to table ${tableName}`, error);
        throw error;
      }
    }
  };

  /* FOR TESTING PURPOSES */
  public populateTable = async (tableName: string) => {
    let repetitions = 22000;

    try {
      while (repetitions > 0) {
        const randomNumber = Math.random() * 10000000;
        const itemToInsert = {
          pk: { S: `PK#${randomNumber}` },
          sk: { S: `SK#${randomNumber}` },
          data: data,
          createdAt: { S: new Date().toISOString() },
          updatedAt: { S: new Date().toISOString() },
          status: { BOOL: true },
          type: { S: 'role' },
        };
        const params: PutItemCommandInput = {
          TableName: tableName,
          Item: itemToInsert,
        };

        const command = new PutItemCommand(params);
        const result = await this.client.send(command);
        console.log(
          result.$metadata.httpStatusCode,
          `Item inserted to table ${tableName}`,
        );
        console.log(repetitions, 'repetitions left');

        repetitions--;
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  };
}
