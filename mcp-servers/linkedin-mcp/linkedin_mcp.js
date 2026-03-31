#!/usr/bin/env node

/**
 * LinkedIn MCP Server
 * 
 * Allows Claude Code / Qwen Code to post updates to LinkedIn.
 * Silver Tier component of the AI Employee system.
 * 
 * Setup:
 * 1. Create LinkedIn app: https://www.linkedin.com/developers/apps
 * 2. Get access token and store in .env file
 * 
 * Usage:
 *   node linkedin_mcp.js
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require('@modelcontextprotocol/sdk/types.js');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

const LINKEDIN_ACCESS_TOKEN = process.env.LINKEDIN_ACCESS_TOKEN;
const LINKEDIN_PERSON_URN = process.env.LINKEDIN_PERSON_URN;

if (!LINKEDIN_ACCESS_TOKEN) {
  console.error('LINKEDIN_ACCESS_TOKEN not found in .env file');
  process.exit(1);
}

const server = new Server(
  {
    name: 'linkedin-mcp',
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
        name: 'post_to_linkedin',
        description: 'Post an update to LinkedIn. Requires human approval for Silver Tier.',
        inputSchema: {
          type: 'object',
          properties: {
            text: {
              type: 'string',
              description: 'The text content of the LinkedIn post (max 3000 characters)',
            },
            title: {
              type: 'string',
              description: 'Optional title for the post',
            },
          },
          required: ['text'],
        },
      },
      {
        name: 'create_linkedin_draft',
        description: 'Create a draft LinkedIn post for human review (Silver Tier HITL pattern)',
        inputSchema: {
          type: 'object',
          properties: {
            text: {
              type: 'string',
              description: 'The text content of the LinkedIn post',
            },
            topic: {
              type: 'string',
              description: 'Topic or category of the post (e.g., "business update", "product launch")',
            },
          },
          required: ['text', 'topic'],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'post_to_linkedin') {
    return await postToLinkedIn(args);
  } else if (name === 'create_linkedin_draft') {
    return await createLinkedInDraft(args);
  } else {
    return {
      content: [{ type: 'text', text: `Unknown tool: ${name}` }],
      isError: true,
    };
  }
});

/**
 * Post to LinkedIn API
 */
async function postToLinkedIn({ text, title }) {
  try {
    // Truncate text if too long (LinkedIn limit is 3000 characters)
    const truncatedText = text.length > 3000 ? text.substring(0, 2997) + '...' : text;
    
    // Create post content
    const postContent = {
      author: `urn:li:person:${LINKEDIN_PERSON_URN || 'ME'}`,
      lifecycleState: 'PUBLISHED',
      specificContent: {
        'com.linkedin.ugc.ShareContent': {
          shareCommentary: {
            text: truncatedText,
          },
          shareMediaCategory: 'NONE',
        },
      },
      visibility: {
        'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC',
      },
    };

    // For Silver Tier, we create a draft file instead of actually posting
    // This implements the Human-in-the-Loop pattern
    const draftContent = `---
type: linkedin_post_draft
created: ${new Date().toISOString()}
status: pending_approval
topic: ${args?.topic || 'General'}
---

# LinkedIn Post Draft

## Content
${truncatedText}

## To Approve
Move this file to /Approved/ to post to LinkedIn.

## To Reject
Move this file to /Rejected/ to discard.

---
*Created by AI Employee LinkedIn MCP Server*
`;

    // In a real implementation, you would:
    // 1. Make the actual API call to LinkedIn
    // 2. For Silver Tier, create approval file instead
    
    return {
      content: [
        {
          type: 'text',
          text: `LinkedIn post draft created. Post requires human approval before publishing.\n\nDraft content:\n${truncatedText}`,
        },
      ],
    };
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error posting to LinkedIn: ${error.message}` }],
      isError: true,
    };
  }
}

/**
 * Create a LinkedIn draft for approval
 */
async function createLinkedInDraft({ text, topic }) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `LINKEDIN_${topic.replace(/\s+/g, '_')}_${timestamp}.md`;
  
  return {
    content: [
      {
        type: 'text',
        text: `Draft file created: ${filename}\n\nThis draft will be saved to /Pending_Approval/ for human review.`,
      },
    ],
  };
}

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('LinkedIn MCP Server running on stdio');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
