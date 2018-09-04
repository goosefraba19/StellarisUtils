using System;
using System.Collections.Generic;
using System.Text;

namespace Stellaris.Convert
{
    public struct Token
    {
        public readonly TokenType Type;
        public readonly string Value;

        public Token(TokenType type) : this(type, null) { }

        public Token(TokenType type, string value)
        {
            this.Type = type;
            this.Value = value;
        }

        public override string ToString()
        {
            return $"Token({this.Type},{this.Value})";
        }
    }
}
