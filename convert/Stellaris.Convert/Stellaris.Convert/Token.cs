using System;
using System.Collections.Generic;
using System.Text;

namespace Stellaris.Convert
{
    public struct Token
    {
        public readonly string Type;
        public readonly string Value;

        public Token(string type) : this(type, null) { }

        public Token(string type, string value)
        {
            this.Type = type;
            this.Value = value ?? "None";
        }

        public override string ToString()
        {
            return $"Token({this.Type},{this.Value})";
        }
    }
}
