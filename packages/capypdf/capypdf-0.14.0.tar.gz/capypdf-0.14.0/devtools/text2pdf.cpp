// SPDX-License-Identifier: Apache-2.0
// Copyright 2024 Jussi Pakkanen

#include <capypdf.hpp>

int main(int argc, char **argv) {
    if(argc != 4) {
        printf("%s <font file> <pdf output> <text to render>\n", argv[0]);
    }
    capypdf::DocumentProperties dp;
    capypdf::PageProperties pp;
    pp.set_pagebox(CAPY_BOX_MEDIA, 0, 0, 200, 200);
    dp.set_default_page_properties(pp);
    dp.set_title("Image generator test");
    capypdf::Generator gen(argv[2], dp);
    auto fontid = gen.load_font(argv[1]);
    auto ctx = gen.new_page_context();
    ctx.render_text(argv[3], fontid, 12, 10, 100);
    gen.add_page(ctx);
    gen.write();

    return 0;
}
