/*
 * Copyright (c) 2024, Tai Nguyen <nguyentritai@gmail.com>
 */
#ifndef __NVPARAM_H__
#define __NVPARAM_H__
/*  NV Paramters macros/definitions */
/* PARAM_ID_0 */
#define DEFAULT_PARAM_ID_0	0x12340000
#define NVP_FIELD_0_BIT	0
#define NVP_Field_0_GET(x)	(((x) >> 0) & 0xffffffff)
union param_id_0 {
	struct {
		uint32_t field_0 : 32;	/* offset 0 */
	};

	uint32_t data;
};

/* PARAM_ID_1 */
#define DEFAULT_PARAM_ID_1	0x00004567
#define NVP_FIELD_0_BIT	0
#define NVP_Field_0_GET(x)	(((x) >> 0) & 0x000fffff)
#define NVP_FIELD_1_BIT	31
#define NVP_Field_1_GET(x)	(((x) >> 31) & 0x00000001)
union param_id_1 {
	struct {
		uint32_t field_0 : 20;	/* offset 0 */
		uint32_t reserved1 : 11;	/* offset 20 */
		uint32_t field_1 : 1;	/* offset 31 */
	};

	uint32_t data;
};

/* PARAM_ID_2 */
#define DEFAULT_PARAM_ID_2	0x12344567
#define NVP_FIELD_0_BIT	0
#define NVP_Field_0_GET(x)	(((x) >> 0) & 0x00000001)
#define NVP_FIELD_1_BIT	1
#define NVP_Field_1_GET(x)	(((x) >> 1) & 0x00007fff)
#define NVP_FIELD_2_BIT	16
#define NVP_Field_2_GET(x)	(((x) >> 16) & 0x00000001)
union param_id_2 {
	struct {
		uint32_t field_0 : 1;	/* offset 0 */
		uint32_t field_1 : 15;	/* offset 1 */
		uint32_t field_2 : 1;	/* offset 16 */
	};

	uint32_t data;
};

#endif /* __NVPARAM_H__ */