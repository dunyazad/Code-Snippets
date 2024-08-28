QMatrix4x4 interpolateMatrices(const QMatrix4x4& a, const QMatrix4x4& b, float t) {
			QVector3D translationA = a.column(3).toVector3D();
			QVector3D translationB = b.column(3).toVector3D();

			QVector3D translationInterpolated = (1 - t) * translationA + t * translationB;

			QVector3D scaleA(
				a.column(0).toVector3D().length(),
				a.column(1).toVector3D().length(),
				a.column(2).toVector3D().length()
			);
			QVector3D scaleB(
				b.column(0).toVector3D().length(),
				b.column(1).toVector3D().length(),
				b.column(2).toVector3D().length()
			);

			QVector3D scaleInterpolated = (1 - t) * scaleA + t * scaleB;

			QMatrix3x3 rotationMatrixA = a.toGenericMatrix<3, 3>();
			QMatrix3x3 rotationMatrixB = b.toGenericMatrix<3, 3>();

			QQuaternion rotationA = QQuaternion::fromRotationMatrix(rotationMatrixA);
			QQuaternion rotationB = QQuaternion::fromRotationMatrix(rotationMatrixB);

			QQuaternion rotationInterpolated = QQuaternion::slerp(rotationA, rotationB, t);

			QMatrix4x4 result;
			result.setToIdentity();

			result.rotate(rotationInterpolated);

			result.scale(scaleInterpolated);

			result.setColumn(3, QVector4D(translationInterpolated, 1.0f));

			return result;
		}
