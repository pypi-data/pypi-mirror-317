#ifndef __NV_CONFIG_H
#define __NV_CONFIG_H

#ifdef __GNUC__
// gcc
#define NV_ENABLE_CUDA   0  // CUDA���g����
#define NV_ENABLE_CLOCK  0  // nv_clock���g����
#define NV_ENABLE_SLEEP  0  // nv_sleep���g����
#ifdef __SSE2__
#define NV_ENABLE_SSE2   1  // SSE2���g����
#else
#define NV_ENABLE_SSE2   0
#endif
#define NV_ENABLE_OPENCV 0  // OpenCV�ϊ����g����
#define NV_XS            1  // Perl�p

#else
// VC++
#define NV_ENABLE_CUDA   1  // CUDA���g����
#define NV_ENABLE_CLOCK  1  // nv_clock���g����
#define NV_ENABLE_SLEEP  1  // nv_sleep���g����
#define NV_ENABLE_SSE2   1  // SSE2���g����
#define NV_ENABLE_OPENCV 1  // OpenCV�ϊ����g����
#define NV_XS            0  // Perl�p

#endif
#endif
