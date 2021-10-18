#!/usr/bin/env node
import 'source-map-support/register'
import * as cdk from '@aws-cdk/core'
import { LambdaStack } from './lambda-stack'
import { getAwsAccount, getAwsRegion } from './utils'

const awsEnv = { account: getAwsAccount(), region: getAwsRegion() }

const app = new cdk.App()

new LambdaStack(app, 'GithubChecksLambda', {
  awsEnv
})