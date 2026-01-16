/**
 * Node publisher service using node-queue-bus.
 * NOTE: Hardcoded config for local testing; use env/config in production.
 */
const { bus: Bus } = require("node-queue-bus");

const connection = {
  pkg: "ioredis",
  host: "127.0.0.1",
  port: 6379,
  db: 0,
  namespace: "resque",
};

const log = (msg) => console.log(`[NODE PUB ${new Date().toISOString()}] ${msg}`);

const bus = new Bus({ connection });

bus.connect(() => {
  const payload = { msg: "hello from node", ts: Date.now() };
  bus.publish("node_event", payload, () => {
    log(`Published node_event -> ${JSON.stringify(payload)}`);
  });

  setTimeout(() => process.exit(0), 200);
});
