#ifndef __NV_FACE_ANALYZE_H
#define __NV_FACE_ANALYZE_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
	// ��̏c���� 
	// x/y ���傫���ق�(�΂߂̏ꍇ�Жڂ��c���ɂȂ邽��)
	float eye_ratio;
	// (��̏�`�A�S)/(��c��-�{���牺�̒���)
	float face_ratio;
	// �Ⴉ����̊Ԃ̕��ϐF
	nv_color_t skin_bgr;
	nv_color_t skin_ec;
	// ��̏ォ����3�{�܂ŕ���F�ŃN���X�^�����O�����Ƃ�
	// ���Ɨ���Ă���ő�v�f�̃N���X�̕��ϐF
	nv_color_t hair_bgr;
	nv_color_t hair_ec;
	// �ڂ̐F���N���X�^�����O���������������4�F
	nv_color_t left_eye_bgr[4];
	nv_color_t right_eye_bgr[4];
	nv_color_t eye_bgr[4];
	// �ڂ̐F���N���X�^�����O���������������4�F(euclidean_color)
	nv_color_t left_eye_ec[4];
	nv_color_t right_eye_ec[4];
	nv_color_t eye_ec[4];
} nv_face_feature_t;

void 
nv_face_analyze(nv_face_feature_t *feature,
				const nv_face_position_t *face,
				const nv_matrix_t *img);


#ifdef __cplusplus
}
#endif
#endif