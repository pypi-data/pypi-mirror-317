import { Task, TaskRunOptions } from '@src';
import { ProtocolFeesWithdrawerDeployment } from './input';

export default async (task: Task, { force, from }: TaskRunOptions = {}): Promise<void> => {
  const input = task.input() as ProtocolFeesWithdrawerDeployment;

  const args = [input.Vault, input.InitialDeniedTokens];
  await task.deployAndVerify('ProtocolFeesWithdrawer', args, from, force);
};
