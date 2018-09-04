using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace Stellaris.Convert
{
    public class Lexer
    {

        private readonly StreamReader reader;
        private int next;

        private StringBuilder builder = new StringBuilder();

        public Lexer(StreamReader reader)
        {
            this.reader = reader;
            this.next = this.reader.Read();
        }

        public Token Token()
        {
            while (true)
            {
                if (this.next == -1)
                {
                    return new Token(TokenType.EOF);
                }

                var c = (char)this.next;

                switch (c)
                {
                    case '\t':
                    case '\n':
                    case ' ':
                        this.next = this.reader.Read();
                        continue;
                    case '{':
                        this.next = this.reader.Read();
                        return new Token(TokenType.LeftCurly);
                    case '}':
                        this.next = this.reader.Read();
                        return new Token(TokenType.RightCurly);
                    case '=':
                        this.next = this.reader.Read();
                        return new Token(TokenType.Equals);
                    case '\"':
                        return new Token(TokenType.Text, this.GetEscapedString());
                }

                if (this.IsValidTextCharacter(c))
                {
                    return new Token(TokenType.Text, this.GetTextString(c));
                }

                throw new Exception("Could not find matching token.");
            }
        }

        private bool IsValidTextCharacter(char c)
        {
            // [a-zA-Z0-9_:.@-]
            return ('a' <= c && c <= 'z') ||
                   ('A' <= c && c <= 'Z') ||
                   ('0' <= c && c <= '9') ||
                   (c == '_') ||
                   (c == ':') ||
                   (c == '.') ||
                   (c == '@') ||
                   (c == '-');
        }

        private string GetTextString(char first)
        {
            this.builder.Clear();
            this.builder.Append(first);

            while (true)
            {
                this.next = this.reader.Read();
                if (this.next == -1)
                {
                    throw new Exception("ERROR: EOF in GetEscapedString?");
                }

                char c = (char)this.next;
                if (this.IsValidTextCharacter(c))
                {
                    this.builder.Append(c);
                }
                else
                {
                    return this.builder.ToString();
                }
            }
        }

        private string GetEscapedString()
        {
            this.builder.Clear();

            while (true)
            {
                this.next = this.reader.Read();

                if (this.next == -1)
                {
                    throw new Exception("ERROR: EOF in GetEscapedString?");
                }

                char c = (char)this.next;
                if (c == '\"')
                {
                    this.next = this.reader.Read();
                    return this.builder.ToString();
                }
                else
                {
                    this.builder.Append(c);
                }
            }
        }
    }
}
