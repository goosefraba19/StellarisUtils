using System;
using System.Collections.Generic;
using System.Text;

namespace Stellaris.Convert
{
    public enum TokenType
    {
        Undefined = 0,
        Equals,
        LeftCurly,
        RightCurly,
        Text,
        EOF
    }
}
