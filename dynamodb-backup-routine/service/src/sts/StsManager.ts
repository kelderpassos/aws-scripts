import {
  STSClient,
  GetCallerIdentityCommand,
  AssumeRoleCommand,
} from '@aws-sdk/client-sts';
import { RoleToAssume, Credentials } from '../helpers/interfaces';
import axios from 'axios';
import { SLACK_WEBHOOK_URL } from '../helpers/constants';

export class StsManager {
  private readonly client: STSClient;

  constructor(
    private region: string,
    private credentials: RoleToAssume,
  ) {
    this.client = new STSClient({ region: this.region });
  }

  public readonly assumeRole = async () => {
    const command = new AssumeRoleCommand(this.credentials);

    try {
      const { Credentials } = await this.client.send(command);
      return {
        accessKeyId: Credentials?.AccessKeyId,
        secretAccessKey: Credentials?.SecretAccessKey,
        sessionToken: Credentials?.SessionToken,
      } as Credentials;
    } catch (error: any) {
      console.log('Error assuming role', error);

      await axios.post(SLACK_WEBHOOK_URL, {
        Message: `Erro ao assumir papel do IAM.
        Nome: ${error.name}, Erro: ${error.message}`,
      });
      throw error;
    }
  };

  public readonly getAccountInfo = async () => {
    const command = new GetCallerIdentityCommand({});
    try {
      return await this.client.send(command);
    } catch (error) {
      console.error(`Erro ao obter informações da conta: ${error}`);
    }
  };
}
