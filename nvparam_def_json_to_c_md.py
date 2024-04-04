#!/usr/bin/env python3

#
# Copyright (c) 2024, Tai Nguyen <nguyentritai@gmail.com>
#
#
import sys
import os
import json

def param_md_content_gen(params):
    md_text = "# Non Voilatile Parameters\n"
    # Generate param table
    md_param_tbl_text = "| Param Index | Param Name | Description |\n"
    md_param_tbl_text += "| --- | --- | --- |\n"
    #Generate bit fields with descriptions
    md_fld_text = ""
    for param in params:
        param_hdr_anchor = str.lower(param['Name'])
        md_param_tbl_text += f"|{param['Index']}|[{param['Name']}](#{param_hdr_anchor})|{param['Description']}|\n"
        # On gitlab, header anchors are generated automatically, so make sure header text is unique
        # md_fld_text += f"## {param['Name']} {{#{param_hdr_anchor}}}\n"
        md_fld_text += f"## {param['Name']}\n"
        md_fld_text += f"- **NV Parameter Index**: {param['Index']}\n"
        md_fld_text += f"- **Category**: {param['Category']}\n"
        md_fld_text += f"- **Description**: {param['Description']}\n"
        md_fld_text += f"- **Bit Fields**:\n\n"
        fields = param['Bits']
        #Construct the table for Bit Fields
        md_fld_text += "| Bits range | Field Name | Field Description |\n"
        md_fld_text += "|---|---|---|\n"
        for field in fields:
            bitpos = field['Position']
            bitsize = field['Bit size']
            if bitsize == 1:
                bitrange = str(bitpos)
            else:
                bitrange = f"{str(bitpos)}-{str(bitpos + bitsize -1)}"
            md_fld_text += f"|{bitrange}|{field['Field Name']}|{field['Description']}|\n"
    
    md_param_tbl_text += "---\n"
    md_text += md_param_tbl_text
    md_text += md_fld_text

    return md_text

C_H_HEADER = "/*\n"
C_H_HEADER += " * Copyright (c) 2024, Tai Nguyen <nguyentritai@gmail.com>\n"
C_H_HEADER += " */\n"
C_H_HEADER += "#ifndef __NVPARAM_H__\n"
C_H_HEADER += "#define __NVPARAM_H__\n"
C_H_END = "#endif /* __NVPARAM_H__ */"

def param_c_content_gen(params):
    c_text = C_H_HEADER
    #
    # Format for macros, definitions
    #   DEFAULT_<PARAM_NAME>
    #   NVP_<PARAM_FIELD0_NAME>_BIT
    #   NVP_<PARAM_FIELD0_NAME>_GET
    # ...
    #   NVP_<PARAM_FIELDn_NAME>_BIT
    #   NVP_<PARAM_FIELDn_NAME>_GET
    #
    # Format for structure with bit fields
    # union <param_name> {
    #   struct {
    #     uint32_t bit_field0 : bitsize0;
    #     uint32_t bit_field1 : bitsize1;
    #     ...
    #     uint32_t bit_fieldN : bitsizeN;
    #   };
    #
    #   uint32_t data;
    # };
    #
    c_text += "/*  NV Paramters macros/definitions */\n"
    for param in params:
        c_text += f"/* {param['Name']} */\n"
        c_text += f"#define DEFAULT_{param['Name']}\t{param['Default value']}\n"
        c_struct = f"union {str.lower(param['Name'])} {{" + "\n"
        c_struct += "\tstruct {\n"
        next_field_pos = 0
        reserved_field_index = 0
        fields = param['Bits']
        for field in fields:
            field_name = field['Field Name']
            bitpos = field['Position']
            bitsize = field['Bit size']
            bitmask = (1 << bitsize) - 1
            c_text += f"#define NVP_{str.upper(field_name)}_BIT\t{str(bitpos)}\n"
            c_text += "#define NVP_{}_GET(x)\t(((x) >> {:d}) & 0x{:08x})\n".format(field_name, bitpos, bitmask)
            # Handle Reserved field
            if next_field_pos != 0 and next_field_pos != bitpos:
                c_struct += f"\t\tuint32_t reserved{reserved_field_index} : {bitpos - next_field_pos};\t/* offset {next_field_pos} */\n"
            c_struct += f"\t\tuint32_t {str.lower(field_name)} : {bitsize};\t/* offset {bitpos} */\n"
            next_field_pos = bitpos + bitsize
            reserved_field_index += 1
        c_struct += "\t};\n\n"
        c_struct += "\tuint32_t data;\n"
        # Add Cstruct to the text    
        c_struct += "};\n\n"
        c_text += c_struct
    c_text += C_H_END

    return c_text

def main():
    #Syntax check
    if len(sys.argv) == 1:
        fname = os.path.basename(__file__)
        print("Syntax Error!")
        print("Usage:")
        print("\t{} <JSON file>".format(fname))
        exit(-1)
    
    fname_json = sys.argv[1]
    try:
        with open(fname_json) as file:
            pass
    except IOError as e:
        print("Unable to open file {}".format(fname_json))
        exit(-1)
    print("JSON file: {}".format(fname_json))

    with open(fname_json, 'r', encoding='utf8') as f_json_input:
        data = json.load(f_json_input)
        # print(data)
        parameters = data['Parameter List']

        #Gen Mark Down to display
        md_fname = fname_json.replace(".json", ".md")
        md_content = param_md_content_gen(parameters)
        print("Generating {} Mark Down file...".format(md_fname))
        with open(md_fname, 'w') as md_file:
            md_file.write(md_content)

        #Gen C header file for dev
        c_fname = fname_json.replace(".json", ".h")
        c_content = param_c_content_gen(parameters)
        print("Generating {} C header file...".format(c_fname))
        with open(c_fname, 'w') as c_file:
            c_file.write(c_content)

if __name__ == "__main__":
    main()