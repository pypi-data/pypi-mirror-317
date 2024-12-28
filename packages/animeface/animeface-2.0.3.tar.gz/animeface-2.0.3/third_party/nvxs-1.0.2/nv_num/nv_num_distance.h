#ifndef __NV_NUM_DISTANCE_H
#define __NV_NUM_DISTANCE_H
#include "nv_core.h"
#include "nv_num_cov.h"

#ifdef __cplusplus
extern "C" {
#endif

// ���[�N���b�h����
float nv_euclidean(const nv_matrix_t *vec1, int m1, const nv_matrix_t *vec2, int m2);
// ���[�N���b�h����^2
float nv_euclidean2(const nv_matrix_t *vec1, int m1, const nv_matrix_t *vec2, int m2);
// �}�n���m�r�X����
float nv_mahalanobis(const nv_cov_t *cov, const nv_matrix_t *x, int xm);

#ifdef __cplusplus
}
#endif

#endif
