/**
 * Aurora WASM Client Integration
 * 
 * This file demonstrates how to integrate the Aurora WASM client
 * with the existing Aurora Portal web interface.
 */

import init, { 
  create_agent, 
  get_version, 
  health_check,
  AuroraAgent 
} from '/wasm-client/pkg/aurora_wasm_client.js?v=3';

class AuroraPortal {
  constructor() {
    this.agent = null;
    this.config = {
      relay_nodes: [
        '/dns4/relay1.aurora.network/tcp/443/wss/p2p/12D3KooWABC',
        '/dns4/relay2.aurora.network/tcp/443/wss/p2p/12D3KooWDEF'
      ],
      blockchain_rpc: 'https://rpc.aurora.network',
      bootstrap_models: [
        '0x1234abcd...', // Discovery model
        '0x5678ef01...', // Negotiation model
        '0x9012cdef...'  // Security model
      ],
      user_did: null
    };
  }

  /**
   * Initialize the Aurora Portal
   */
  async initialize() {
    try {
      console.log('Initializing Aurora Portal...');
      
      // Show loading state
      this.showStatus('Initializing...', 'info');

      // Initialize WASM module
      await init();
      console.log('WASM module loaded successfully');
      console.log('Aurora Client Version:', get_version());
      console.log('Health check:', health_check());

      // Create Aurora agent
      this.agent = await create_agent(JSON.stringify(this.config));
      console.log('Aurora Agent created');

      // Start the agent (connect to P2P + blockchain)
      await this.agent.start();
      console.log('Aurora Agent started');

      // Get agent info
      const did = this.agent.get_did();
      const peerCount = this.agent.get_peer_count();
      const state = this.agent.get_state();

      console.log('Agent DID:', did);
      console.log('Connected peers:', peerCount);
      console.log('Agent state:', state);

      // Update UI
      this.showStatus(`Connected as ${did.slice(0, 20)}...`, 'success');
      this.updatePeerCount(peerCount);
      this.updateDID(did);
      this.enableChat();

      return true;
    } catch (error) {
      console.error('Failed to initialize Aurora Portal:', error);
      this.showStatus('Failed to initialize: ' + error.message, 'error');
      return false;
    }
  }

  /**
   * Process user prompt
   */
  async processPrompt(prompt) {
    if (!this.agent) {
      throw new Error('Agent not initialized');
    }

    try {
      this.showStatus('Processing...', 'info');
      
      const result = await this.agent.process_prompt(prompt);
      
      this.showStatus('Ready', 'success');
      return result;
    } catch (error) {
      console.error('Failed to process prompt:', error);
      this.showStatus('Error: ' + error.message, 'error');
      throw error;
    }
  }

  /**
   * Get current agent state
   */
  getState() {
    if (!this.agent) return null;
    return this.agent.get_state();
  }

  /**
   * Shutdown the portal
   */
  async shutdown() {
    if (this.agent) {
      try {
        await this.agent.shutdown();
        console.log('Aurora Agent shut down');
      } catch (error) {
        console.error('Error shutting down agent:', error);
      }
    }
  }

  // UI Helper methods
  showStatus(message, type) {
    const statusEl = document.getElementById('status');
    if (statusEl) {
      statusEl.textContent = message;
      statusEl.className = `status ${type}`;
    }
    console.log(`[${type.toUpperCase()}] ${message}`);
  }

  updatePeerCount(count) {
    const peerCountEl = document.getElementById('peer-count');
    if (peerCountEl) {
      peerCountEl.textContent = count;
    }
  }

  updateDID(did) {
    // Update short DID in info row (if element exists in future)
    const didEl = document.getElementById('did');
    if (didEl) {
      didEl.textContent = did.slice(0, 20) + '...';
    }
  }

  enableChat() {
    const chatInput = document.getElementById('chat-input');
    const chatButton = document.getElementById('chat-button');
    
    if (chatInput) chatInput.disabled = false;
    if (chatButton) chatButton.disabled = false;
  }
}

// Global portal instance
let portal = null;

  /**
   * Initialize Aurora Portal when page loads
   */
  window.addEventListener('DOMContentLoaded', async () => {
    console.log('Aurora Portal loading...');
    
    portal = new AuroraPortal();
    
    // Initialize portal
    const success = await portal.initialize();
    
    if (success) {
      console.log('Aurora Portal ready!');
      setupEventListeners();
      setupIdentityUI();
    }
  });/**
 * Setup UI event listeners
 */
function setupEventListeners() {
  const chatButton = document.getElementById('chat-button');
  const chatInput = document.getElementById('chat-input');

  if (chatButton && chatInput) {
    chatButton.addEventListener('click', async () => {
      const prompt = chatInput.value.trim();
      if (!prompt) return;

      try {
        const result = await portal.processPrompt(prompt);
        displayMessage('user', prompt);
        displayMessage('agent', result);
        chatInput.value = '';
      } catch (error) {
        displayMessage('system', 'Error: ' + error.message);
      }
    });

    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chatButton.click();
      }
    });
  }
}

/**
 * Display a chat message
 */
function displayMessage(role, content) {
  const chatHistory = document.getElementById('chat-history');
  if (!chatHistory) return;

  const messageEl = document.createElement('div');
  messageEl.className = `message ${role}`;
  messageEl.textContent = content;
  
  chatHistory.appendChild(messageEl);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}

  /**
   * Setup identity UI and action buttons
   */
  function setupIdentityUI() {
    console.log('Setting up identity UI...');
    
    const identityPanel = document.getElementById('identity-panel');
    const didFullEl = document.getElementById('did-full');
    const identityTypeEl = document.getElementById('identity-type');
    
    console.log('Identity panel element:', identityPanel);
    console.log('Portal agent:', portal.agent);
    
    if (identityPanel && portal.agent) {
      // Show identity panel
      identityPanel.style.display = 'block';
      console.log('✅ Identity panel displayed');
      
      // Display full DID
      const did = portal.agent.get_did();
      if (didFullEl) didFullEl.textContent = did;
      if (identityTypeEl) identityTypeEl.textContent = 'Decentralized';
      
      // Test Signature button
      const btnSignTest = document.getElementById('btn-sign-test');
      if (btnSignTest) {
        btnSignTest.addEventListener('click', async () => {
          try {
            btnSignTest.disabled = true;
            btnSignTest.textContent = '🔐 Signing...';
            
            const message = `Test signature from ${did} at ${new Date().toISOString()}`;
            console.log('📝 Signing message:', message);
            
            const signature = await portal.agent.sign_message(message);
            console.log('✅ Signature:', signature.substring(0, 32) + '...');
            console.log('   Length:', signature.length / 2, 'bytes');
            
            // Verify
            const { verify_signature } = await import('/wasm-client/pkg/aurora_wasm_client.js?v=3');
            const publicKey = portal.agent.get_public_key();
            const isValid = await verify_signature(publicKey, message, signature);
            
            if (isValid) {
              alert(`✅ Signature Test Successful!\n\nMessage: ${message.substring(0, 60)}...\n\nSignature: ${signature.substring(0, 40)}...\n\nLength: ${signature.length / 2} bytes\n\nVerification: VALID ✓`);
            } else {
              alert('❌ Signature verification failed!');
            }
            
          } catch (error) {
            console.error('Signature test failed:', error);
            alert('❌ Signature test failed: ' + error.message);
          } finally {
            btnSignTest.disabled = false;
            btnSignTest.textContent = '🖊️ Test Signature';
          }
        });
      }
      
      // Export Identity button
      const btnExport = document.getElementById('btn-export-identity');
      if (btnExport) {
        btnExport.addEventListener('click', async () => {
          try {
            // Ask for password to encrypt private key
            const password = prompt(
              '🔐 Set a password to encrypt your private key:\n\n' +
              'This password will be required to restore your identity.\n' +
              'Keep it safe - there is NO password recovery!'
            );
            
            if (!password || password.length < 8) {
              alert('❌ Password must be at least 8 characters!');
              return;
            }
            
            const confirmPassword = prompt('🔐 Confirm your password:');
            if (password !== confirmPassword) {
              alert('❌ Passwords do not match!');
              return;
            }
            
            btnExport.disabled = true;
            btnExport.textContent = '🔐 Encrypting...';
            
            const did = portal.agent.get_did();
            const publicKey = portal.agent.get_public_key();
            const privateKeyJWK = localStorage.getItem('aurora_private_key_jwk');
            
            if (!privateKeyJWK) {
              alert('❌ Private key not found in localStorage!');
              return;
            }
            
            // Encrypt private key with password (simple XOR for now, AES in Phase 1)
            const encryptedPrivateKey = await encryptWithPassword(privateKeyJWK, password);
            
            const identity = {
              version: '2.0',
              type: 'full-backup',
              did: did,
              publicKey: JSON.parse(publicKey),
              encryptedPrivateKey: encryptedPrivateKey,
              algorithm: 'ECDSA-P256',
              encryption: 'PBKDF2-AES-GCM',
              created: new Date().toISOString(),
              warning: '⚠️ This file contains your encrypted private key. Keep it safe and NEVER share it!'
            };
            
            const blob = new Blob([JSON.stringify(identity, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `aurora-identity-backup-${did.split(':').pop().substring(0, 8)}.json`;
            a.click();
            URL.revokeObjectURL(url);
            
            console.log('✅ Full identity backup exported (encrypted)');
            alert('✅ Identity backup saved!\n\n⚠️ IMPORTANT:\n• Store this file safely\n• Remember your password\n• Both are required to restore');
            
          } catch (error) {
            console.error('Export failed:', error);
            alert('❌ Export failed: ' + error.message);
          } finally {
            btnExport.disabled = false;
            btnExport.textContent = '📥 Export Identity';
          }
        });
      }
      
      // Import Identity button
      const btnImport = document.getElementById('btn-import-identity');
      if (btnImport) {
        btnImport.addEventListener('click', async () => {
          try {
            // Create file input
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = 'application/json,.json';
            
            input.onchange = async (e) => {
              try {
                const file = e.target.files[0];
                if (!file) return;
                
                btnImport.disabled = true;
                btnImport.textContent = '📂 Reading...';
                
                const text = await file.text();
                const backup = JSON.parse(text);
                
                // Validate backup format
                if (!backup.version || !backup.encryptedPrivateKey) {
                  alert('❌ Invalid backup file format!\n\nThis doesn\'t appear to be an Aurora identity backup.');
                  return;
                }
                
                if (backup.version !== '2.0') {
                  alert('❌ Incompatible backup version!\n\nThis backup was created with a different version.');
                  return;
                }
                
                // Ask for password
                const password = prompt('🔐 Enter the password to decrypt your private key:');
                if (!password) return;
                
                btnImport.textContent = '🔓 Decrypting...';
                
                // Decrypt private key
                const privateKeyJWK = await decryptWithPassword(backup.encryptedPrivateKey, password);
                
                // Validate it's valid JSON
                JSON.parse(privateKeyJWK);
                
                // Confirm before overwriting
                const currentDID = localStorage.getItem('aurora_identity');
                if (currentDID) {
                  const confirm = window.confirm(
                    '⚠️ You already have an identity!\n\n' +
                    'Importing will REPLACE your current identity.\n\n' +
                    'Current DID: ' + portal.agent.get_did().substring(0, 40) + '...\n' +
                    'Backup DID: ' + backup.did.substring(0, 40) + '...\n\n' +
                    'Continue?'
                  );
                  
                  if (!confirm) return;
                }
                
                btnImport.textContent = '💾 Restoring...';
                
                // Store decrypted keys
                localStorage.setItem('aurora_private_key_jwk', privateKeyJWK);
                localStorage.setItem('aurora_identity', JSON.stringify({
                  did: backup.did,
                  public_key_jwk: JSON.stringify(backup.publicKey)
                }));
                
                console.log('✅ Identity restored from backup');
                alert('✅ Identity Restored Successfully!\n\nDID: ' + backup.did + '\n\nPage will reload...');
                
                window.location.reload();
                
              } catch (error) {
                console.error('Import failed:', error);
                if (error.message.includes('Decryption failed')) {
                  alert('❌ Wrong password or corrupted backup file!');
                } else {
                  alert('❌ Import failed: ' + error.message);
                }
              } finally {
                btnImport.disabled = false;
                btnImport.textContent = '📤 Import Backup';
              }
            };
            
            input.click();
            
          } catch (error) {
            console.error('Import setup failed:', error);
            alert('❌ Import failed: ' + error.message);
          }
        });
      }
      
      // Reset Identity button
      const btnReset = document.getElementById('btn-reset-identity');
      if (btnReset) {
        btnReset.addEventListener('click', async () => {
          const confirmed = confirm(
            '⚠️ WARNING: Reset Identity?\n\n' +
            'This will delete your current decentralized identity.\n' +
            'You will lose access to:\n' +
            '- Your DID\n' +
            '- Your signing keys\n' +
            '- Any reputation associated with this identity\n\n' +
            'A new identity will be generated on next reload.\n\n' +
            'Are you sure?'
          );
          
          if (confirmed) {
            try {
              // Clear localStorage
              localStorage.removeItem('aurora_identity');
              localStorage.removeItem('aurora_private_key_jwk');
              
              console.log('✅ Identity reset. Reloading...');
              alert('✅ Identity deleted. Page will reload to generate a new identity.');
              
              window.location.reload();
            } catch (error) {
              console.error('Reset failed:', error);
              alert('❌ Reset failed: ' + error.message);
            }
          }
        });
      }
    }
  }

  /**
   * Encrypt data with password using Web Crypto API
   */
  async function encryptWithPassword(data, password) {
    // Derive key from password
    const encoder = new TextEncoder();
    const passwordData = encoder.encode(password);
    
    const keyMaterial = await crypto.subtle.importKey(
      'raw',
      passwordData,
      'PBKDF2',
      false,
      ['deriveKey']
    );
    
    const salt = crypto.getRandomValues(new Uint8Array(16));
    const key = await crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: salt,
        iterations: 100000,
        hash: 'SHA-256'
      },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt']
    );
    
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const dataBuffer = encoder.encode(data);
    
    const encryptedBuffer = await crypto.subtle.encrypt(
      { name: 'AES-GCM', iv: iv },
      key,
      dataBuffer
    );
    
    // Combine salt + iv + encrypted data
    const result = new Uint8Array(salt.length + iv.length + encryptedBuffer.byteLength);
    result.set(salt, 0);
    result.set(iv, salt.length);
    result.set(new Uint8Array(encryptedBuffer), salt.length + iv.length);
    
    // Return as base64
    return btoa(String.fromCharCode(...result));
  }
  
  /**
   * Decrypt data with password
   */
  async function decryptWithPassword(encryptedData, password) {
    try {
      // Decode base64
      const combined = Uint8Array.from(atob(encryptedData), c => c.charCodeAt(0));
      
      const salt = combined.slice(0, 16);
      const iv = combined.slice(16, 28);
      const data = combined.slice(28);
      
      // Derive key from password
      const encoder = new TextEncoder();
      const passwordData = encoder.encode(password);
      
      const keyMaterial = await crypto.subtle.importKey(
        'raw',
        passwordData,
        'PBKDF2',
        false,
        ['deriveKey']
      );
      
      const key = await crypto.subtle.deriveKey(
        {
          name: 'PBKDF2',
          salt: salt,
          iterations: 100000,
          hash: 'SHA-256'
        },
        keyMaterial,
        { name: 'AES-GCM', length: 256 },
        false,
        ['decrypt']
      );
      
      const decryptedBuffer = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv: iv },
        key,
        data
      );
      
      const decoder = new TextDecoder();
      return decoder.decode(decryptedBuffer);
      
    } catch (error) {
      throw new Error('Decryption failed - wrong password or corrupted file');
    }
  }

  /**
   * Cleanup on page unload
   */
  window.addEventListener('beforeunload', () => {
    if (portal) {
      portal.shutdown();
    }
  });

  // Export for external use
  export { AuroraPortal, portal };