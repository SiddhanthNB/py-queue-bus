/**
 * Node subscriber service using node-queue-bus.
 * NOTE: Hardcoded config for local testing; use env/config in production.
 */
const { rider: Rider, bus: Bus } = require("node-queue-bus");

const connection = {
  pkg: "ioredis",
  host: "127.0.0.1",
  port: 6379,
  db: 0,
  namespace: "resque",
};

const appKey = "node_service";
const priority = "default";
const queueName = `${appKey}_${priority}`;

const log = (msg) => console.log(`[NODE SUB ${new Date().toISOString()}] ${msg}`);

const bus = new Bus({ connection });
bus.connect(() => {
  bus.subscribe(appKey, priority, "handle_python_event", { bus_event_type: "python_event" });
  bus.subscribe(appKey, priority, "handle_python_event_delayed", { bus_event_type: "python_event_delayed" });
  bus.subscribe(appKey, priority, "handle_python_event_scheduled", { bus_event_type: "python_event_scheduled" });
  bus.subscribe(appKey, priority, "handle_node_event", { bus_event_type: "node_event" });
  bus.subscribe(appKey, priority, "handle_heartbeat", { bus_event_type: "heartbeat_minutes" });
  log(`Subscribed to events on queue ${queueName}`);

  const jobs = {
    handle_python_event: {
      perform: (payload, cb) => {
        log(`handle_python_event received payload: ${JSON.stringify(payload)}`);
        cb();
      },
    },
    handle_python_event_delayed: {
      perform: (payload, cb) => {
        log(`handle_python_event_delayed received payload: ${JSON.stringify(payload)}`);
        cb();
      },
    },
    handle_python_event_scheduled: {
      perform: (payload, cb) => {
        log(`handle_python_event_scheduled received payload: ${JSON.stringify(payload)}`);
        cb();
      },
    },
    handle_node_event: {
      perform: (payload, cb) => {
        log(`handle_node_event received payload: ${JSON.stringify(payload)}`);
        cb();
      },
    },
    handle_heartbeat: {
      perform: (payload, cb) => {
        log(`handle_heartbeat received payload: ${JSON.stringify(payload)}`);
        cb();
      },
    },
  };

  const rider = new Rider({ connection, queues: [queueName], toDrive: true }, jobs);
  rider.connect(() => {
    log("Starting rider...");
    rider.workerCleanup();
    rider.start();
  });
});
