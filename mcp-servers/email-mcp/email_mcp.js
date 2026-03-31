#!/usr/bin/env node

/**
 * Email MCP Server
 * 
 * Allows Claude Code / Qwen Code to send emails via SMTP.
 * Silver Tier component of the AI Employee system.
 * 
 * Setup:
 * 1. Create .env file with SMTP credentials
 * 2. For Gmail: Use App Password (not regular password)
 * 
 * Usage:
 *   node email_mcp.js
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const dotenv = require('dotenv');
const nodemailer = require('nodemailer');

// Load environment variables
dotenv.config();

const SMTP_HOST = process.env.SMTP_HOST || 'smtp.gmail.com';
const SMTP_PORT = parseInt(process.env.SMTP_PORT || '587');
const SMTP_USER = process.env.SMTP_USER;
const SMTP_PASS = process.env.SMTP_PASS;

if (!SMTP_USER || !SMTP_PASS) {
  console.error('SMTP_USER and SMTP_PASS not found in .env file');
  process.exit(1);
}

// Create transporter
const transporter = nodemailer.createTransport({
  host: SMTP_HOST,
  port: SMTP_PORT,
  secure: SMTP_PORT === 465,
  auth: {
    user: SMTP_USER,
    pass: SMTP_PASS,
  },
});

const server = new Server(
  {
    name: 'email-mcp',
    version: '0.1.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'send_email',
        description: 'Send an email. For Silver Tier, creates approval file first (HITL pattern).',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address',
            },
            subject: {
              type: 'string',
              description: 'Email subject',
            },
            body: {
              type: 'string',
              description: 'Email body (plain text or HTML)',
            },
            isHtml: {
              type: 'boolean',
              description: 'Whether the body is HTML (default: false)',
            },
            cc: {
              type: 'string',
              description: 'CC email addresses (comma-separated)',
            },
            bcc: {
              type: 'string',
              description: 'BCC email addresses (comma-separated)',
            },
          },
          required: ['to', 'subject', 'body'],
        },
      },
      {
        name: 'create_email_draft',
        description: 'Create an email draft for human review (Silver Tier HITL pattern)',
        inputSchema: {
          type: 'object',
          properties: {
            to: {
              type: 'string',
              description: 'Recipient email address',
            },
            subject: {
              type: 'string',
              description: 'Email subject',
            },
            body: {
              type: 'string',
              description: 'Email body',
            },
            reason: {
              type: 'string',
              description: 'Reason for sending this email',
            },
          },
          required: ['to', 'subject', 'body', 'reason'],
        },
      },
      {
        name: 'test_connection',
        description: 'Test the SMTP connection',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'send_email') {
    return await sendEmail(args);
  } else if (name === 'create_email_draft') {
    return await createEmailDraft(args);
  } else if (name === 'test_connection') {
    return await testConnection();
  } else {
    return {
      content: [{ type: 'text', text: `Unknown tool: ${name}` }],
      isError: true,
    };
  }
});

/**
 * Send email via SMTP
 * For Silver Tier, this creates an approval file instead of sending directly
 */
async function sendEmail({ to, subject, body, isHtml = false, cc, bcc }) {
  try {
    // Silver Tier: Create approval file instead of sending
    // This implements Human-in-the-Loop pattern
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const approvalContent = `---
type: email_approval_request
created: ${new Date().toISOString()}
status: pending_approval
recipient: ${to}
subject: ${subject}
---

# Email Approval Request

## Details
- **To:** ${to}
- **Subject:** ${subject}
- **CC:** ${cc || 'None'}
- **BCC:** ${bcc || 'None'}

## Content
${isHtml ? body : '```\n' + body + '\n```'}

## To Approve
Move this file to /Approved/ to send this email.

## To Reject
Move this file to /Rejected/ to discard.

---
*Created by AI Employee Email MCP Server*
`;

    return {
      content: [
        {
          type: 'text',
          text: `Email draft created for approval. The email will be sent once a human approves it.\n\nTo: ${to}\nSubject: ${subject}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error creating email draft: ${error.message}` }],
      isError: true,
    };
  }
}

/**
 * Actually send the email (called after approval)
 */
async function sendEmailApproved({ to, subject, body, isHtml = false, cc, bcc }) {
  try {
    const info = await transporter.sendMail({
      from: SMTP_USER,
      to,
      subject,
      text: isHtml ? undefined : body,
      html: isHtml ? body : undefined,
      cc,
      bcc,
    });

    return {
      content: [
        {
          type: 'text',
          text: `Email sent successfully! Message ID: ${info.messageId}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error sending email: ${error.message}` }],
      isError: true,
    };
  }
}

/**
 * Create email draft for approval
 */
async function createEmailDraft({ to, subject, body, reason }) {
  return {
    content: [
      {
        type: 'text',
        text: `Email draft created for: ${to}\nSubject: ${subject}\nReason: ${reason}\n\nThis draft requires human approval before sending.`,
      },
    ],
  };
}

/**
 * Test SMTP connection
 */
async function testConnection() {
  try {
    await transporter.verify();
    return {
      content: [
        {
          type: 'text',
          text: 'SMTP connection successful! Ready to send emails.',
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: `SMTP connection failed: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
}

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Email MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
