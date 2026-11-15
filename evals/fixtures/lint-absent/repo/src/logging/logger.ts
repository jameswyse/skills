import { stderr } from "node:process";

type LogFields = Readonly<Record<string, string | number | boolean>>;

function write(level: "info" | "warn" | "error", message: string, fields: LogFields): void {
  stderr.write(`${JSON.stringify({ level, message, ...fields })}\n`);
}

export const logger = {
  info: (message: string, fields: LogFields = {}): void => {
    write("info", message, fields);
  },
  warn: (message: string, fields: LogFields = {}): void => {
    write("warn", message, fields);
  },
  error: (message: string, fields: LogFields = {}): void => {
    write("error", message, fields);
  },
};
