import { getDesignTokens } from './themePrimitives';
import {
    chartsCustomizations,
    dataGridCustomizations,
    datePickersCustomizations,
    treeViewCustomizations,
    inputsCustomizations,
    dataDisplayCustomizations,
    feedbackCustomizations,
    navigationCustomizations,
    surfacesCustomizations,
} from './customizations';

export default function getTheme(mode) {
    return {
        ...getDesignTokens(mode),
        components: {
            ...chartsCustomizations,
            ...dataGridCustomizations,
            ...datePickersCustomizations,
            ...treeViewCustomizations,
            ...inputsCustomizations,
            ...inputsCustomizations,
            ...dataDisplayCustomizations,
            ...feedbackCustomizations,
            ...navigationCustomizations,
            ...surfacesCustomizations,
        },
    };
}
