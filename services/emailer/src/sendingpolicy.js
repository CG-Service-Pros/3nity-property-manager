export function emailSendingEnabled(env) {
  return env.ALLOW_SENDING_EMAILS === 'true';
}
