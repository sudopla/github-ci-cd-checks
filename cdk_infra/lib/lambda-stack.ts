/**
 * Application Stack
 */

import * as fs from 'fs'
import * as path from 'path'
import * as events from '@aws-cdk/aws-events'
import * as event_targets from '@aws-cdk/aws-events-targets'
import * as iam from '@aws-cdk/aws-iam'
import * as lambda from '@aws-cdk/aws-lambda'
import { PythonFunction } from '@aws-cdk/aws-lambda-python'
import * as cdk from '@aws-cdk/core'

export interface LambdaStackProps {
  awsEnv: { account: string, region: string }
}

export class LambdaStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props: LambdaStackProps) {
    super(scope, id, {
      description: 'Lambda to check Github Release and PRs status',
      env: props.awsEnv
    })

    const func = new PythonFunction(this, 'GithubLambda', {
      functionName: 'github_cicd_checks_lambda',
      entry: path.join(__dirname, '..', '..', 'lambda'),
      index: 'index.py',
      handler: 'handler',
      runtime: lambda.Runtime.PYTHON_3_7,
      timeout: cdk.Duration.seconds(30)
    })

    // Give Lambda access to secrets to retrieve Github and Slack tokens

    // Get the secret names from config file
    const data = fs.readFileSync(path.join(__dirname, '..', '..', 'lambda', 'app', 'config.py'), 'utf8')
    const lines = data.split('\n')
    const reg1 = /^GITHUB_ACCESS_TOKEN_SECRET_NAME\s*=\s*"(.*)"/
    const reg2 = /^SLACK_APP_TOKEN_SECRET_NAME\s*=\s*"(.*)"/
    let githubTokenName = ''
    let slackTokenName = ''
    for (let l of lines) {
      let reg1_match = l.match(reg1)
      let reg2_match = l.match(reg2)
      if (reg1_match) {
        githubTokenName = reg1_match[1]
      }
      if (reg2_match) {
        slackTokenName = reg2_match[1]
      }
    }

    func.addToRolePolicy(new iam.PolicyStatement({
      actions: ['secretsmanager:GetSecretValue'],
      resources: [
        `arn:aws:secretsmanager:${this.region}:${this.account}:secret:${githubTokenName}-*`,
        `arn:aws:secretsmanager:${this.region}:${this.account}:secret:${slackTokenName}-*`
      ]
    }))

    // Run Lambda on schedule
    new events.Rule(this, 'RunLambda', {
      schedule: events.Schedule.cron({ weekDay: 'MON-FRI', hour: '12-22/4', minute: '0' }), // Time is in UTC
      targets: [new event_targets.LambdaFunction(func)]
    })

  }
}
