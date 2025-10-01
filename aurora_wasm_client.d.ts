/* tslint:disable */
/* eslint-disable */
/**
 * Initialize the Aurora WASM client
 * This is the entry point called from JavaScript
 */
export function main(): void;
/**
 * Create a new Aurora Agent instance
 */
export function create_agent(config: any): Promise<AuroraAgent>;
/**
 * Get the version of the Aurora client
 */
export function get_version(): string;
/**
 * Health check function
 */
export function health_check(): boolean;
/**
 * Sign a message with the agent's private key
 */
export function sign_message(agent: AuroraAgent, message: string): Promise<string>;
/**
 * Verify a signature
 */
export function verify_signature(public_key_jwk: string, message: string, signature: string): Promise<boolean>;
/**
 * The main Aurora Intelligence System agent
 */
export class AuroraAgent {
  private constructor();
  free(): void;
  [Symbol.dispose](): void;
  /**
   * Create a new Aurora Agent
   */
  static new(config_json: string): Promise<AuroraAgent>;
  /**
   * Start the agent (connect to P2P network and blockchain)
   */
  start(): Promise<void>;
  /**
   * Process a user prompt
   */
  process_prompt(prompt: string): Promise<string>;
  /**
   * Get current agent state
   */
  get_state(): any;
  /**
   * Get user DID
   */
  get_did(): string;
  /**
   * Get connected peer count
   */
  get_peer_count(): number;
  /**
   * Get public key in JWK format
   */
  get_public_key(): string;
  /**
   * Sign a message using the user's private key
   * Returns the signature as a hex-encoded string
   */
  sign_message(message: string): Promise<string>;
  /**
   * Verify a signature (static method)
   * This can be called by other peers to verify messages
   */
  static verify_signature(public_key_jwk: string, message: string, hex_signature: string): Promise<boolean>;
  /**
   * Shutdown the agent
   */
  shutdown(): Promise<void>;
}

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly __wbg_auroraagent_free: (a: number, b: number) => void;
  readonly auroraagent_new: (a: number, b: number) => any;
  readonly auroraagent_start: (a: number) => any;
  readonly auroraagent_process_prompt: (a: number, b: number, c: number) => any;
  readonly auroraagent_get_state: (a: number) => any;
  readonly auroraagent_get_did: (a: number) => [number, number];
  readonly auroraagent_get_peer_count: (a: number) => number;
  readonly auroraagent_get_public_key: (a: number) => [number, number];
  readonly auroraagent_sign_message: (a: number, b: number, c: number) => any;
  readonly auroraagent_verify_signature: (a: number, b: number, c: number, d: number, e: number, f: number) => any;
  readonly auroraagent_shutdown: (a: number) => any;
  readonly main: () => void;
  readonly create_agent: (a: any) => any;
  readonly get_version: () => [number, number];
  readonly health_check: () => number;
  readonly sign_message: (a: number, b: number, c: number) => any;
  readonly verify_signature: (a: number, b: number, c: number, d: number, e: number, f: number) => any;
  readonly __wbindgen_exn_store: (a: number) => void;
  readonly __externref_table_alloc: () => number;
  readonly __wbindgen_export_2: WebAssembly.Table;
  readonly __wbindgen_malloc: (a: number, b: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number, d: number) => number;
  readonly __wbindgen_export_5: WebAssembly.Table;
  readonly __wbindgen_free: (a: number, b: number, c: number) => void;
  readonly closure80_externref_shim: (a: number, b: number, c: any) => void;
  readonly closure105_externref_shim: (a: number, b: number, c: any, d: any) => void;
  readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;
/**
* Instantiates the given `module`, which can either be bytes or
* a precompiled `WebAssembly.Module`.
*
* @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
*
* @returns {InitOutput}
*/
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
*
* @returns {Promise<InitOutput>}
*/
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
